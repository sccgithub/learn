# https://www.kaggle.com/learn/machine-learning
import pandas as pd

from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

mel_data = pd.read_csv('./melb_data.csv')
# mel_data = pd.read_csv('./train.csv')

res = mel_data.describe()

# mel_data = mel_data.dropna(axis=0)

# res = mel_data.columns

y = mel_data.Price

mel_features = ['Rooms', 'Bathroom', 'Landsize', 'Lattitude', 'Longtitude']

X = mel_data[mel_features]

# res = X.describe()

# res = X.head()

# 应用决策树模型
mel_model = DecisionTreeRegressor(random_state=1)
mel_model.fit(X, y)

# 测试
# print("Making predictions for the following 5 houses:")
# print(X.head())
# print("The predictions are")
# print(mel_model.predict(X.head()))

# 验证模型
predicted_home_prices = mel_model.predict(X)
res = mean_absolute_error(y, predicted_home_prices)

train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
mel_model = DecisionTreeRegressor()
mel_model.fit(train_X, train_y)
val_predictions = mel_model.predict(val_X)
res = mean_absolute_error(val_y, val_predictions)
# print(res)

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
  model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
  model.fit(train_X, train_y)
  preds_val = model.predict(val_X)
  mae = mean_absolute_error(val_y, preds_val)
  return (mae)

# for max_leaf_nodes in [5, 50, 500, 5000]:
#   my_mae = get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y)
#   print("Max leaf nodes: %d  \t\t Mean Absolute Error:  %d" %(max_leaf_nodes, my_mae))

model = RandomForestRegressor(random_state=1)
model.fit(train_X, train_y)
mel_preds = model.predict(val_X)
res = mean_absolute_error(val_y, mel_preds)
# print(res)
