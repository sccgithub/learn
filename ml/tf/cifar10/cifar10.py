from __future__ import absolute_import, print_function, division
import re
import cifar10_input
import tensorflow as tf

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_integer('batch_size', 128,\
  """Number of images to process in a batch.""")

tf.app.flags.DEFINE_boolean('use_fp16', False,\
  """Train the model using fp16.""")

IMAGE_SIZE = cifar10_input.IMAGE_SIZE
NUM_CLASSES = cifar10_input.NUM_CLASSES
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = cifar10_input.NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = cifar10_input.NUM_EXAMPLES_PER_EPOCH_FOR_EVAL

# 训练过程中的常亮
# 用于移动平均线的衰减
MOVING_AVERAGE_DECAY = 0.9999
# 学习速率下降的周期
NUM_EPOCHS_PER_DECAY = 350.0
# 学习速率衰减因子
LEARNING_RATE_DECAY_FACTOR = 0.1
# 初始学习速率
INITIAL_LEARNING_RATE = 0.1

TOWER_NAME = 'tower'

def _variable_on_cpu(name, shape, initializer):
  """在CPU内存初始化变量
  """
  with tf.device('/cpu:0'):
    dtype = tf.float16 if FLAGS.use_fp16 else tf.float32
    var = tf.get_variable(name, shape, initializer=initializer, dtype=dtype)
  return var

def _variable_with_weight_decay(name, shape, stddev, wd):
  """创建带衰减的初始化变量
      初始化为带截断的正太分布，只有在指定了衰减权重时才会衰减
      ARGS：
        name:变量名
        shape：变量形状
        stddev：截断的高斯标准差
        wd: L2 loss 衰减系数
  """
  dtype = tf.float16 if FLAGS.use_fp16 else tf.float32
  var = _variable_on_cpu(name, shape,\
    tf.truncated_normal_initializer(stddev=stddev, dtype=dtype))
  if wd is not None:
    weight_decay = tf.multiply(tf.nn.l2_loss(var), wd, name='weight_loss')
    tf.add_to_collection('losses', weight_decay)
  return var

def _activation_summary(x):
  # 为激活生成简介
  tensor_name = re.sub('%s_[0-9]*/' % TOWER_NAME, '', x.op.name)
  tf.summary.histogram(tensor_name + '/activations', x)
  tf.summary.scalar(tensor_name + '/sparsity', tf.nn.zero_fraction(x))

def inerfence(images):
  """
  构建模型
  """
  # 使用tf.get_variable()而不是tf.Variable()
  # 因为前者可以在多GPU共享变量

  # 第一层，卷积1
  with tf.variable_scope('conv1') as scope:
    # 生成第一层的卷积核 5*5
    kernel = _variable_with_weight_decay('weights',
    shape=[5, 5, 3, 64], stddev=5e-2, wd=None)
    conv = tf.nn.conv2d(images, kernel, [1, 1, 1, 1], padding='SAME')
    # 初始化偏置量
    biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.0))
    pre_activation = tf.nn.bias_add(conv, biases)
    # 使用relu激活函数
    conv1 = tf.nn.relu(pre_activation, name=scope.name)
    _activation_summary(conv1)
  
  # 第二层，最大值池化1
  pool1 = tf.nn.max_pool(conv1, ksize=[1, 3, 3, 1], strides=[1, 2, 2, 1],
  padding='SAME', name='pool1')

  # 第三层， 标准化层1
  norm1 = tf.nn.lrn(pool1, 4, bias=1.0, alpha=0.001/9, beta=0.75, name='norm1')

  # 第四层， 卷积2
  with tf.variable_scope('conv2')as scope:
    kernel = _variable_with_weight_decay('weights', shape=[5, 5, 64, 64],
    stddev=5e-2, wd=None)
    conv = tf.nn.conv2d(norm1, kernel, [1, 1, 1, 1], padding='SAME')
    biases = _variable_on_cpu('biases', [64], tf.constant_initializer(0.1))
    pre_activation = tf.nn.bias_add(conv, biases)
    conv2 = tf.nn.relu(pre_activation, name=scope.name)
    _activation_summary(conv2)
  
  #第五层， 标准化2
  norm2 = tf.nn.lrn(conv2, 4, bias=1.0, alpha=0.001 / 9.0, beta=0.75,
                    name='norm2')
  
  # 第六层， 最大池化2
  pool2 = tf.nn.max_pool(norm2, ksize=[1, 3, 3, 1],
                         strides=[1, 2, 2, 1], padding='SAME', name='pool2')

  # 第七层， 全连接层1
  with tf.variable_scope('local3') as scope:
    # 将输入展平，方便后面做矩阵乘法
    reshape = tf.keras.layers.Flatten()(pool2)
    dim = reshape.get_shape()[1].value
    weights = _variable_with_weight_decay('weights', shape=[dim, 384],
    stddev=0.04, wd=0.004)
    biases = _variable_on_cpu('biases', [384], tf.constant_initializer(0.1))
    local3 = tf.nn.relu(tf.matmul(reshape, weights) + biases, name=scope.name)
    _activation_summary(local3)

  # 第8层， 全连接层2
  with tf.variable_scope('local4') as scope:
    weights = _variable_with_weight_decay('weights', shape=[384, 192],
                                          stddev=0.04, wd=0.004)
    biases = _variable_on_cpu('biases', [192], tf.constant_initializer(0.1))
    local4 = tf.nn.relu(tf.matmul(local3, weights) + biases, name=scope.name)
    _activation_summary(local4)

  # 第9层，softmax分类器
  with tf.variable_scope('softmax_linear') as scope:
    weights = _variable_with_weight_decay('weights', [192, NUM_CLASSES],
                                          stddev=1/192.0, wd=None)
    biases = _variable_on_cpu('biases', [NUM_CLASSES],
                              tf.constant_initializer(0.0))
    softmax_linear = tf.add(tf.matmul(local4, weights), biases, name=scope.name)
    _activation_summary(softmax_linear)

  return softmax_linear

def inputs(eval_data):
  """Construct input for CIFAR evaluation using the Reader ops.

  Args:
    eval_data: bool, indicating if one should use the train or eval data set.

  Returns:
    images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.
  """
  images, labels = cifar10_input.inputs(eval_data=eval_data,
                                        batch_size=FLAGS.batch_size)
  if FLAGS.use_fp16:
    images = tf.cast(images, tf.float16)
    labels = tf.cast(labels, tf.float16)
  return images, labels