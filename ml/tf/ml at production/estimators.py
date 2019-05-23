import tensorflow as tf
# 特征列支持
import tensorflow.feature_column as fc
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

import sys
import matplotlib.pyplot as plt
from IPython.display import clear_output

tf.enable_eager_execution()

models_path = os.path.join(os.getcwd(), 'models')

sys.path.append(models_path)

# from 

