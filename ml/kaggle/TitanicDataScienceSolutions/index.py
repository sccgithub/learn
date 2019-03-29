# https://www.kaggle.com/startupsci/titanic-data-science-solutions
# Ignore warnings
import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import random as rnd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import seaborn as sns
# import matplotlib.pyplot as plt

# %matplotlib inline

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier

# load data
train_df = pd.read_csv('./train.csv')
test_df = pd.read_csv('./test.csv')

combine = [train_df, test_df]

# print(train_df.columns.values)
# desc = train_df.describe(include=['O'])
# print(desc)
# print('-' * 40)
# print(test_df.info())

sortedd = train_df[['Pclass', 'Survived']].groupby(['Pclass'], as_index=False).mean().sort_values(by="Survived", ascending=False)

# 简单数据分析
# train_df[["Sex", "Survived"]].groupby(['Sex'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# train_df[["SibSp", "Survived"]].groupby(['SibSp'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# train_df[["Parch", "Survived"]].groupby(['Parch'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# print(sortedd)

# # 概率分析幸存与年龄的关系
# g = sns.FacetGrid(train_df, col='Survived')
# g.map(plt.hist, 'Age', bins=20)
# # 展示图像
# plt.show()

# 绘图展示多个特征（数值|类别）的相关性
# g = sns.FacetGrid(train_df, col='Survived', row='Pclass', size=2.2, aspect=1.6)
# g.map(plt.hist, 'Age', alpha=.5, bins=20)
# g.add_legend()
# plt.show()

# 关联分析
# grid = sns.FacetGrid(train_df, row='Embarked', size=2.2, aspect=1.6)
# grid.map(sns.pointplot, 'Pclass', 'Survived', 'Sex', palette='deep')
# grid.add_legend()
# plt.show()

# 分类特征与数值特征的相关性
# grid = sns.FacetGrid(train_df, row='Embarked', col='Survived', size=2.2, aspect=1.6)
# grid.map(sns.barplot, 'Sex', 'Fare', alpha=.5, ci=None)
# grid.add_legend()
# plt.show()

# 删除无用属性
# print("Before", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

train_df = train_df.drop(['Ticket', 'Cabin'], axis=1)
test_df = test_df.drop(['Ticket', 'Cabin'], axis=1)
combine = [train_df, test_df]

# print("After", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

# 身份信息统计、整理
for dataset in combine:
    dataset['Title'] = dataset.Name.str.extract(' ([A-Za-z]+)\.', expand=False)

# pd.crosstab(train_df['Title'], train_df['Sex'])

# 身份信息合并
for dataset in combine:
  dataset['Title'] = dataset['Title'].replace(['Lady', 'Countess','Capt', 'Col',\
  'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
  dataset['Title'] = dataset['Title'].replace('Mlle', 'Miss')
  dataset['Title'] = dataset['Title'].replace('Ms', 'Miss')
  dataset['Title'] = dataset['Title'].replace('Mme', 'Mrs')

# res = train_df[['Title', 'Survived']].groupby(['Title'], as_index=False).mean()
# print(res)

# 数值化身份信息
title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
for dataset in combine:
    dataset['Title'] = dataset['Title'].map(title_mapping)
    dataset['Title'] = dataset['Title'].fillna(0)
# print(train_df.head())

# 删除无用属性
train_df = train_df.drop(['Name', 'PassengerId'], axis=1)
test_df = test_df.drop(['Name'], axis=1)
combine = [train_df, test_df]
# print("After2", train_df.shape, test_df.shape, combine[0].shape, combine[1].shape)

# 转换属性，性别转为数值
for dataset in combine:
    dataset['Sex'] = dataset['Sex'].map( {'female': 1, 'male': 0} ).astype(int)

# print(train_df.head())

# 填充空值，使用平均值和标准差之间的随机数
# grid = sns.FacetGrid(train_df, row='Pclass', col='Sex', size=2.2, aspect=1.6)
# grid.map(plt.hist, 'Age', alpha=.5, bins=20)
# grid.add_legend()
# plt.show()

guess_ages = np.zeros((2,3))

for dataset in combine:
  for i in range(0, 2):
    for j in range(0, 3):
      guess_df = dataset[(dataset['Sex'] == i) &\
      (dataset['Pclass'] == j + 1)]['Age'].dropna()
      age_guess = guess_df.median()

      guess_ages[i, j] = int(age_guess / 0.5 + 0.5) * 0.5

  for i in range(0, 2):
    for j in range(0, 3):
      dataset.loc[(dataset.Age.isnull()) & (dataset.Sex == i) & (dataset.Pclass == j + 1), \
      'Age'] = guess_ages[i, j]
    
  dataset['Age'] = dataset['Age'].astype(int)

# print(train_df.head())


# 年龄段与存活率的相关性
train_df['AgeBand'] = pd.cut(train_df['Age'], 5)
# res = train_df[['AgeBand', 'Survived']].groupby(['AgeBand'], as_index=False).mean().sort_values(by='AgeBand', ascending=True)
# print(res)

#用年龄段标记年龄
for dataset in combine:    
    dataset.loc[ dataset['Age'] <= 16, 'Age'] = 0
    dataset.loc[(dataset['Age'] > 16) & (dataset['Age'] <= 32), 'Age'] = 1
    dataset.loc[(dataset['Age'] > 32) & (dataset['Age'] <= 48), 'Age'] = 2
    dataset.loc[(dataset['Age'] > 48) & (dataset['Age'] <= 64), 'Age'] = 3
    dataset.loc[ dataset['Age'] > 64, 'Age']
# print(train_df.head())

# 删除AgeBand
train_df = train_df.drop(['AgeBand'], axis=1)
combine = [train_df, test_df]

# 创建家庭人数字段
for dataset in combine:
    dataset['FamilySize'] = dataset['SibSp'] + dataset['Parch'] + 1

# res = train_df[['FamilySize', 'Survived']].groupby(['FamilySize'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# print(res)

# 创建是否单独字段
for dataset in combine:
    dataset['IsAlone'] = 0
    dataset.loc[dataset['FamilySize'] == 1, 'IsAlone'] = 1

# res = train_df[['IsAlone', 'Survived']].groupby(['IsAlone'], as_index=False).mean()
# print(res)

# 有了是否单独之后就可以去掉SibSp，Parch，FamilySize
train_df = train_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
test_df = test_df.drop(['Parch', 'SibSp', 'FamilySize'], axis=1)
combine = [train_df, test_df]

# 创建一个人工的字段Age*Class
for dataset in combine:
    dataset['Age*Class'] = dataset.Age * dataset.Pclass


# 填充缺少的两个Embarked
freq_port = train_df.Embarked.dropna().mode()[0]
for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].fillna(freq_port)
    
# res = train_df[['Embarked', 'Survived']].groupby(['Embarked'], as_index=False).mean().sort_values(by='Survived', ascending=False)
# print(res)

# 将Embarked转换为数字值
for dataset in combine:
    dataset['Embarked'] = dataset['Embarked'].map( {'S': 0, 'C': 1, 'Q': 2} ).astype(int)

# print(train_df.head())

# 填充测试数据的缺省值
test_df['Fare'].fillna(test_df['Fare'].dropna().median(), inplace=True)
# print(test_df.head())


# 创建价格区间
train_df['FareBand'] = pd.qcut(train_df['Fare'], 4)
res = train_df[['FareBand', 'Survived']].groupby(['FareBand'], as_index=False).mean().sort_values(by='FareBand', ascending=True)
# print(res)

# 将价格区间映射到价格
for dataset in combine:
    dataset.loc[ dataset['Fare'] <= 7.91, 'Fare'] = 0
    dataset.loc[(dataset['Fare'] > 7.91) & (dataset['Fare'] <= 14.454), 'Fare'] = 1
    dataset.loc[(dataset['Fare'] > 14.454) & (dataset['Fare'] <= 31), 'Fare']   = 2
    dataset.loc[ dataset['Fare'] > 31, 'Fare'] = 3
    dataset['Fare'] = dataset['Fare'].astype(int)

# 删除价格区间
train_df = train_df.drop(['FareBand'], axis=1)
combine = [train_df, test_df]
    
# print(train_df.head())

# 模型开始
X_train = train_df.drop("Survived", axis=1)
Y_train = train_df["Survived"]
X_test  = test_df.drop("PassengerId", axis=1).copy()
# print(X_train.shape)
# print(Y_train.shape)
# print(X_test.shape)

# 逻辑回归测试
logreg = LogisticRegression()
logreg.fit(X_train, Y_train)
Y_pred = logreg.predict(X_test)
acc_log = round(logreg.score(X_train, Y_train) * 100, 2)
# print(acc_log)

coeff_df = pd.DataFrame(train_df.columns.delete(0))
coeff_df.columns = ['Feature']
coeff_df["Correlation"] = pd.Series(logreg.coef_[0])

res = coeff_df.sort_values(by='Correlation', ascending=False)
# print(res)

# 使用支持向量机进行预测
svc = SVC()
svc.fit(X_train, Y_train)
Y_pred = svc.predict(X_test)
acc_svc = round(svc.score(X_train, Y_train) * 100, 2)
# print(acc_svc)

# knn
knn = KNeighborsClassifier(n_neighbors = 3)
knn.fit(X_train, Y_train)
Y_pred = knn.predict(X_test)
acc_knn = round(knn.score(X_train, Y_train) * 100, 2)
# print(acc_knn)

# 朴素贝叶斯分类器
gaussian = GaussianNB()
gaussian.fit(X_train, Y_train)
Y_pred = gaussian.predict(X_test)
acc_gaussian = round(gaussian.score(X_train, Y_train) * 100, 2)
# print(acc_gaussian)

# 感知器
perceptron = Perceptron()
perceptron.fit(X_train, Y_train)
Y_pred = perceptron.predict(X_test)
acc_perceptron = round(perceptron.score(X_train, Y_train) * 100, 2)
# print(acc_perceptron)

# Linear SVC
linear_svc = LinearSVC()
linear_svc.fit(X_train, Y_train)
Y_pred = linear_svc.predict(X_test)
acc_linear_svc = round(linear_svc.score(X_train, Y_train) * 100, 2)
# print(acc_linear_svc)


# 随机梯度下降法
sgd = SGDClassifier()
sgd.fit(X_train, Y_train)
Y_pred = sgd.predict(X_test)
acc_sgd = round(sgd.score(X_train, Y_train) * 100, 2)
# print(acc_sgd)


# 决策树
decision_tree = DecisionTreeClassifier()
decision_tree.fit(X_train, Y_train)
Y_pred = decision_tree.predict(X_test)
acc_decision_tree = round(decision_tree.score(X_train, Y_train) * 100, 2)
# print(acc_decision_tree)


# 随机森林
random_forest = RandomForestClassifier(n_estimators=100)
random_forest.fit(X_train, Y_train)
Y_pred = random_forest.predict(X_test)
random_forest.score(X_train, Y_train)
acc_random_forest = round(random_forest.score(X_train, Y_train) * 100, 2)
# print(acc_random_forest)


# 对前面的模型进行排名
models = pd.DataFrame({
  'Model': ['Support Vector Machines', 'KNN', 'Logistic Regression', 
            'Random Forest', 'Naive Bayes', 'Perceptron', 
            'Stochastic Gradient Decent', 'Linear SVC', 
            'Decision Tree'],
  'Score': [acc_svc, acc_knn, acc_log, 
            acc_random_forest, acc_gaussian, acc_perceptron, 
            acc_sgd, acc_linear_svc, acc_decision_tree]})
res = models.sort_values(by='Score', ascending=False)
print(res)
# 随机森林最佳

# 生成结果
submission = pd.DataFrame({
  "PassengerId": test_df["PassengerId"],
  "Survived": Y_pred
})
submission.to_csv('./submission.csv', index=False)