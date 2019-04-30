# https://www.kaggle.com/learn/machine-learning
# level 2
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

mel_data = pd.read_csv('./melb_data.csv')

# 查看空值
missing_val_count_by_column = (mel_data.isnull().sum())
# print(missing_val_count_by_column[missing_val_count_by_column > 0])

# 插补法
# copy_data = mel_data.copy()
# # 找出空行
# cols_with_missing = (col for col in copy_data.columns if copy_data[col].isnull().any())
# # 复制空行
# for col in cols_with_missing:
#   copy_data[col + '_was_missing'] = copy_data[col].isnull()

# my_imputer = SimpleImputer()
# copy_data = pd.DataFrame(my_imputer.fit_transform(copy_data))
# # copy_data.columns = mel_data.columns
# print(copy_data.head(10))

mel_target = mel_data.Price
mel_predictors = mel_data.drop(['Price'], axis=1)
mel_numeric_predictors = mel_predictors.select_dtypes(exclude=['object'])

# cols_with_missing = [col for col in X_train.columns if X_train[col].isnull().any()]
# reduced_X_train = X_train.drop(cols_with_missing, axis=1)
# reduced_X_test = X_train.drop(cols_with_missing, axis=1)
# print("Mean Absolute Error from dropping columns with Missing Values:")
# print(score_dataset(reduced_X_train, reduced_X_test, y_train, y_test))
