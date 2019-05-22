import tensorflow as tf
from tensorflow import keras

import numpy as np
import matplotlib.pyplot as plt

print(tf.__version__)

fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
# label 为0-9的数字，对应以下种类
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
print(np.shape(train_images))
print(np.shape(test_images))

# 看一张图
# plt.figure()
# plt.imshow(train_images[0])
# plt.colorbar()
# plt.grid(False)
# plt.show()

# 将0-255的像素值转换到0-1
train_images = train_images / 255
test_images = test_images / 255

# 查看前25张图
# plt.figure(figsize=(10, 10))
# for i in range(25):
#   plt.subplot(5, 5, i + 1)
#   plt.xticks([])
#   plt.yticks([])
#   plt.grid(False)
#   plt.imshow(train_images[i], cmap=plt.cm.binary)
#   plt.xlabel(class_names[train_labels[i]])
# plt.show()

model = keras.Sequential([
  # 第一层将二维图像转换为一维
  keras.layers.Flatten(input_shape=(28, 28)),
  # 第二层为128节点的全连接层
  keras.layers.Dense(128, activation=tf.nn.relu),
  # 第三层为softmax分类器
  keras.layers.Dense(10, activation=tf.nn.softmax)
])

# 设置模型参数
model.compile(
  # 优化器
  optimizer=tf.train.AdamOptimizer(),
  # 损失函数
  loss='sparse_categorical_crossentropy',
  # 在训练和测试期间的模型评估标准
  metrics=['accuracy'])

# 训练模型
model.fit(train_images, train_labels, epochs=5)

# 测试模型
test_loss, test_acc = model.evaluate(test_images, test_labels)

print('Test accuracy:', test_acc)

# 对测试集进行预测
predictions = model.predict(test_images)

print(predictions[0])
