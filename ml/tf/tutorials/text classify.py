import tensorflow as tf
from tensorflow import keras

import numpy as np

print(tf.__version__)

imdb = keras.datasets.imdb
# 加载IMDB数据集
(train_data, train_labels), (test_data, test_labels) = imdb.load_data(num_words=10000)
# 查看数据集规模
# print("Training entries: {}, labels: {}".format(len(train_data), len(train_labels)))

# print(train_data[0])

# 将数据集中文字编号转换为文字
word_index = imdb.get_word_index()
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2  # unknown
word_index["<UNUSED>"] = 3

reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
def decode_review(text):
  word = ' '.join([reverse_word_index.get(i, '?') for i in text])
  print(word)

# 查看转换后的文本
# decode_review(train_data[0])

# 将长短不同的评论数据补齐为相同长度，
train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                        value=word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)
test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                        value=word_index["<PAD>"],
                                                        padding='post',
                                                        maxlen=256)

# 词汇计数
vocab_size = 10000
model = keras.Sequential()
# 第一层为嵌入层，将文本索引值转换为固定尺寸的稠密向量
model.add(keras.layers.Embedding(vocab_size, 16))
# 全局平均池化层
model.add(keras.layers.GlobalAveragePooling1D())
# 16个神经元的全连接层
model.add(keras.layers.Dense(16, activation=tf.nn.relu))
# 最后一层输出0-1之间的概率或置信度
model.add(keras.layers.Dense(1, activation=tf.nn.sigmoid))

# 查看模型概述
print(model.summary())

model.compile(optimizer=tf.train.AdamOptimizer(),
              loss='binary_crossentropy',
              metrics=['accuracy'])

# 从训练集中分割出10000条数据作为验证数据
x_val = train_data[:10000]
partial_x_train = train_data[10000:]

y_val = train_labels[:10000]
partial_y_train = train_labels[10000:]

# 用有 512 个样本的小批次训练模型 40 个周期
# 监控模型在验证集的 10000 个样本上的损失和准确率
history = model.fit(partial_x_train,
          partial_y_train,
          epochs=30,
          batch_size=512,
          validation_data=(x_val, y_val),
          verbose=1)

# 评估模型
results = model.evaluate(test_data, test_labels)

print(results)

# model.fit() 返回一个 History 对象，该对象包含一个字典，其中包括训练期间发生的所有情况
history_dict = history.history
print(history_dict)

import matplotlib.pyplot as plt

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(1, len(acc) + 1)
# "bo" is for "blue dot"
plt.plot(epochs, loss, 'bo', label='Training loss')
# b is for "solid blue line"
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.show()
