from __future__ import print_function, absolute_import, division

import tensorflow as tf
import tensorflow_datasets as tfds

# 图像大小
IMAGE_SIZE = 24

# 总共10类
# airplane, automobile, bird, cat, deer, dog, frog, horse, ship, and truck.
NUM_CLASSES = 10

# 训练集和验证集大小
NUM_EXAMPLES_PER_EPOCH_FOR_TRAIN = 50000
NUM_EXAMPLES_PER_EPOCH_FOR_EVAL = 10000

def _get_image_labels(batch_size, split, distords=False):
  # 按split读取训练集或测试集
  dataset = tfds.load(name='cifar10', split=split)
  scope = 'data_augmentation' if distords else 'input'
  # 图像预处理
  with tf.name_scope(scope):
    dataset = dataset.map(DataPreprocessor(distords), num_parallel_calls=10)
  # 不启用图片预载
  dataset = dataset.prefetch(-1)
  # 重复数据集
  # 这样就有了无限多的示例流、无序排列，以32为一批次
  dataset = dataset.repeat().batch(batch_size)
  # 将数据转为枚举对象
  iterator = dataset.make_one_shot_iterator()
  image_labels = iterator.get_next()
  images, labels = image_labels['input'], image_labels['target']
  tf.summary.image('images', images)
  return images, labels
  


class DataPreprocessor(object):
  def __init__(self, distords):
    self._distords = distords
  def __call__(self, record):
    image = record['image']
    # 数据类型转换为float32
    image = tf.cast(image, tf.float32)
    if self._distords:
      # 将原始图像裁剪为 IMAGE_SIZE * IMAGE_SIZE * 3的张量
      image = tf.random_crop(image, [IMAGE_SIZE, IMAGE_SIZE, 3])
      # 进行失真处理0 从左到右随机翻转图像
      image = tf.image.random_flip_left_right(image)
      # 进行失真处理1 随机调整亮度
      image = tf.image.random_brightness(image, max_delta=63)
      # 进行失真处理2 随机调整对比度
      image = tf.image.random_contrast(image, lower=0.2, upper=1.8)
    else:
      image = tf.image.resize_image_with_crop_or_pad(image, IMAGE_SIZE, IMAGE_SIZE)
    # 使模型对图像的动态范围变化不敏感
    image = tf.image.per_image_standardization(image)
    return dict(input=image, target=record['label'])

def distorted_inputs(batch_size):
  # 测试数据
  """
  Returns:
    images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.
  """
  return _get_image_labels(batch_size, tfds.Split.TRAIN, distords=True)

def inputs(eval_data, batch_size):
  """
  Returns:
    images: Images. 4D tensor of [batch_size, IMAGE_SIZE, IMAGE_SIZE, 3] size.
    labels: Labels. 1D tensor of [batch_size] size.
  """
  # eval_data 指定使用哪个数据集
  split = tfds.Split.TEST if eval_data == 'test' else tfds.Split.TRAIN
  return _get_image_labels(batch_size, split)