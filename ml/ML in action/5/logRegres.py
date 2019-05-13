from numpy import *
import math
import matplotlib.pyplot as plt

def loadDataSet(filename):
  dataMat = []
  labelMat = []
  fr = open(filename)

  for line in fr.readlines():
    lineArr = line.strip().split()
    dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
    labelMat.append(int(lineArr[2]))
  return dataMat, labelMat

def sigmoid(inX):
  return 1.0 / (1 + exp(-inX))

  # return 2 * 1.0 / (1 + exp(-2 * inX)) - 1

def gradAscent(dataMat, classLabels):
  dataMatrix = mat(dataMat)
  labelMat = mat(classLabels).transpose()
  m, n = shape(dataMatrix)

  alpha = 0.001
  maxCycles = 500
  weights = ones((n, 1))

  for k in range(maxCycles):
    h = sigmoid(dataMatrix * weights)
    error = (labelMat - h)
    weights = weights + alpha * dataMatrix.transpose() * error

  return array(weights)

def plotBestFit(dataArr, labelMat, weights):
  n = shape(dataArr)[0]
  xcord1 = []; ycord1 = []
  xcord2 = []; ycord2 = []

  for i in range(n):
    if int(labelMat[i]) == 1:
      xcord1.append(dataArr[i, 1])
      ycord1.append(dataArr[i, 2])
    else:
      xcord2.append(dataArr[i, 1])
      ycord2.append(dataArr[i, 2])
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
  ax.scatter(xcord2, ycord2, s=30, c='green')
  x = arange(-3.0, 3.0, 0.1)
  y = (-weights[0]-weights[1]*x)/weights[2]
  ax.plot(x, y)
  plt.xlabel('X'); plt.ylabel('Y')
  plt.show()

def stocGradAscent0(dataMatrix, classLabels):
  m, n = shape(dataMatrix)
  alpha = 0.01
  weights = ones(n)

  for i in range(m):
    h = sigmoid(sum(dataMatrix[i] * weights))
    error = classLabels[i] - h
    weights = weights + alpha * error * dataMatrix[i]
  return weights

def stocGradAscent1(dataMatrix, classLabels, numIter=150):
  m, n = shape(dataMatrix)
  weights = ones(n)

  for j in range(numIter):
    dataIndex = list(range(m))
    for i in range(m):
      alpha = 4 / (1.0 + i + j) + 0.0001
      randIndex = int(random.uniform(0, len(dataIndex)))
      h = sigmoid(sum(dataMatrix[dataIndex[randIndex]] * weights))
      error = classLabels[dataIndex[randIndex]] - h
      weights = weights + alpha * error * dataMatrix[dataIndex[randIndex]]
      del(dataIndex[randIndex])
  return weights
      

def testLR():
  dataMat, labelMat = loadDataSet('../AiLearning/data/5.Logistic/TestSet.txt')
  dataArr = array(dataMat)
  # weights = gradAscent(dataArr, labelMat)
  weights = stocGradAscent1(dataArr, labelMat, 500)
  plotBestFit(dataArr, labelMat, weights)

def testGrad():
  dataArr, labelArr = loadDataSet('../AiLearning/data/5.Logistic/TestSet.txt')
  # weights = gradAscent(dataArr, labelArr)
  weights = stocGradAscent0(array(dataArr), labelArr)
  print(weights)
testLR() 
# testGrad()