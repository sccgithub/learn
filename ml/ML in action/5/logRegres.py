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


def classifyVector(inX, weights):
  prob = sigmoid(sum(inX * weights))
  if prob > 0.5:
    return 1.0
  else:
    return 0.0

def colicTest():
  frTrain = open('../AiLearning/data/5.Logistic/HorseColicTraining.txt')
  frTest = open('../AiLearning/data/5.Logistic/HorseColicTest.txt')
  trainSet = []
  trainLabels = []
  for line in frTrain.readlines():
    currLine = line.strip().split('\t')
    lineArr = []
    for i in range(21):
      lineArr.append(float(currLine[i]))
    trainSet.append(lineArr)
    trainLabels.append(float(currLine[21]))
  trainWeights = stocGradAscent1(array(trainSet), trainLabels, 500)

  errCount = 0.0
  numTestVec = 0.0
  for line in frTest.readlines():
    numTestVec += 1
    currLine = line.strip().split('\t')
    lineArr = []
    for i in range(21):
        lineArr.append(float(currLine[i]))
    if int(classifyVector(array(lineArr), trainWeights)) != int(currLine[21]):
      errCount += 1
  errRate = (float(errCount) / numTestVec)
  print('the error rate of this test is: ', errRate)
  return errRate

def multiTest():
  numTest = 10
  errSum = 0.0
  for k in range(numTest):
    errSum += colicTest()
  print("after %d iterations the average error rate is: %f" % (numTest, errSum/float(numTest)))

multiTest()
# testLR() 
# testGrad()