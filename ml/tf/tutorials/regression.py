from __future__ import absolute_import, division, print_function
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import pathlib
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

dataset_path = keras.utils.get_file('auto-mpg.data',\
  'https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data')
# print(dataset_path)

column_names = ['MPG','Cylinders','Displacement','Horsepower','Weight',
                'Acceleration', 'Model Year', 'Origin']

raw_dataset = pd.read_csv(dataset_path, names=column_names, na_values='?',\
  comment='\t', sep=' ', skipinitialspace=True)
dataset = raw_dataset.copy()
# print(dataset.tail())

# 查看空值
# print(dataset.isna().sum())

# 去掉含空值的数据
dataset = dataset.dropna()

# 将origin转换为国别
origin = dataset.pop('Origin')

dataset['USA'] = (origin == 1)*1.0
dataset['Europe'] = (origin == 2)*1.0
dataset['Japan'] = (origin == 3)*1.0
# print(dataset.tail())

# 将数据分割为训练集和测试集

train_dataset = dataset.sample(frac=0.8, random_state=0)
test_dataset = dataset.drop(train_dataset.index)

# 查看数据相关性
# sns.pairplot(train_dataset[["MPG", "Cylinders", "Displacement", "Weight"]], diag_kind="kde")
# plt.show()

train_stats = train_dataset.describe()
train_stats.pop("MPG")
train_stats = train_stats.transpose()
# 查看数据概述
# train_stats


train_labels = train_dataset.pop('MPG')
test_labels = test_dataset.pop('MPG')

# 归一化数据
def norm(x):
  return (x - train_stats['mean']) / train_stats['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

def buildModel():
  model = keras.Sequential([
    # 64个神经元的全连接层,输入层
    layers.Dense(64, activation=tf.nn.relu, input_shape=[len(train_dataset.keys())]),
    # 64个神经元的全连接层
    layers.Dense(64, activation=tf.nn.relu),
    # 一个神经元的输出层
    layers.Dense(1)])
  # 优化器
  optimizer = tf.keras.optimizers.RMSprop(0.001)
  model.compile(loss='mean_squared_error',
                optimizer=optimizer,
                metrics=['mean_absolute_error', 'mean_squared_error'])
  return model

model = buildModel()

# print(model.summary())

example_batch = normed_train_data[:10]
example_result = model.predict(example_batch)
# print(example_result)

class PrintDot(keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs):
    if epoch % 100 == 0: print('')
    print('.', end='')

EPOCHS = 1000

history = model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, validation_split = 0.2, verbose=0,
  callbacks=[PrintDot()])

hist = pd.DataFrame(history.history)
hist['epoch'] = history.epoch
print(hist.tail())

def plot_history(history):
  hist = pd.DataFrame(history.history)
  hist['epoch'] = history.epoch
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Abs Error [MPG]')
  plt.plot(hist['epoch'], hist['mean_absolute_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_absolute_error'],
           label = 'Val Error')
  plt.ylim([0,5])
  plt.legend()
  
  plt.figure()
  plt.xlabel('Epoch')
  plt.ylabel('Mean Square Error [$MPG^2$]')
  plt.plot(hist['epoch'], hist['mean_squared_error'],
           label='Train Error')
  plt.plot(hist['epoch'], hist['val_mean_squared_error'],
           label = 'Val Error')
  plt.ylim([0,20])
  plt.legend()
  plt.show()


plot_history(history)



# model = buildModel()

# # The patience parameter is the amount of epochs to check for improvement
# early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)

# history = model.fit(normed_train_data, train_labels, epochs=EPOCHS,
#                     validation_split = 0.2, verbose=0, callbacks=[early_stop, PrintDot()])

# plot_history(history)