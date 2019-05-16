from numpy import *
import matplotlib.pyplot as plt

def loadDataSet(filename):
  numFeat = len(open(filename).readline().split('\t')) - 1
  dataMat = []
  labbelMat = []
  fr = open(filename)
  for line in fr.readlines():
    lineArr = []
    currLine = line.strip().split('\t')
    for i in range(numFeat):
      lineArr.append(float(currLine[i]))
    dataMat.append(lineArr)
    labbelMat.append(float(currLine[-1]))
  return dataMat, labbelMat

def standRegres(xArr, yArr):
  xMat = mat(xArr)
  yMat = mat(yArr).T
  xTx = xMat.T * xMat
  # linalg.det() 函数是用来求得矩阵的行列式的
  # 如果矩阵的行列式为0，则这个矩阵是不可逆的，就无法进行接下来的运算
  if linalg.det(xTx) == 0.0:
    print('this matrix can not do inverse')
    return
  ws = xTx.I * (xMat.T * yMat)
  return ws

def test():
  xArr, yArr = loadDataSet('../AiLearning/data/8.Regression/data.txt')
  ws = standRegres(xArr, yArr)
  xMat = mat(xArr)
  yMat = mat(yArr)
  print(ws)
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.scatter(xMat[:, 1].flatten().A[0], yMat.T[:, 0].flatten().A[0])
  xCopy = xMat.copy()
  xCopy.sort(0)
  yHat = xCopy * ws
  print('相关性')
  print(corrcoef(yHat.T, yMat))
  ax.plot(xCopy[:, 1], yHat)
  plt.show()

def lwlr(testPoint, xArr, yArr, k=1.0):
  xMat = mat(xArr)
  yMat = mat(yArr).T
  m = shape(xMat)[0]
  weights = mat(eye((m)))

  for j in range(m):
    diffMat = testPoint - xMat[j, :]
    weights[j, j] = exp(diffMat * diffMat.T / (-2 * k ** 2))
  xTx = xMat.T * (weights * xMat)
  if linalg.det(xTx) == 0.0:
    print('this matrix can not do inverse')
    return
  ws = xTx.I * (xMat.T * (weights * yMat))
  return testPoint * ws

def lwlrTest(testArr, xArr, yArr, k=1.0):
  m = shape(testArr)[0]
  yHat = zeros(m)
  for i in range(m):
    yHat[i] = lwlr(testArr[i], xArr, yArr, k)
  return yHat

def test2():
  xArr, yArr = loadDataSet('../AiLearning/data/8.Regression/data.txt')
  yHat = lwlrTest(xArr, xArr, yArr, 0.03)
  xMat = mat(xArr)
  strInd = xMat[:, 1].argsort(0)
  xSort = xMat[strInd][:, 0, :]
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(xSort[:, 1], yHat[strInd])
  ax.scatter(xMat[:,1].flatten().A[0], mat(yArr).T.flatten().A[0] , s=2, c='red')
  plt.show()

def rssError(yArr, yHatArr):
  return ((yArr - yHatArr) ** 2).sum()

def abaloneTest():
  abX, abY = loadDataSet('../AiLearning/data/8.Regression/abalone.txt')
  oldyHat01 = lwlrTest(abX[0: 99], abX[0: 99], abY[0: 99], 0.1)
  oldyHat1 = lwlrTest(abX[0: 99], abX[0: 99], abY[0: 99], 1)
  oldyHat10 = lwlrTest(abX[0: 99], abX[0: 99], abY[0: 99], 10)

  print('oldyHat01 error size is:', rssError(abY[0: 99], oldyHat01.T))
  print('oldyHat01 error size is:', rssError(abY[0: 99], oldyHat1.T))
  print('oldyHat01 error size is:', rssError(abY[0: 99], oldyHat10.T))

  newyHat01 = lwlrTest(abX[100:199], abX[0:99], abY[0:99], 0.1)
  newyHat1 = lwlrTest(abX[100:199], abX[0:99], abY[0:99], 1)
  newyHat10 = lwlrTest(abX[100:199], abX[0:99], abY[0:99], 10)
  print('new yHat01 error Size is :' , rssError(abY[0:99], newyHat01.T))
  print('new yHat1 error Size is :' , rssError(abY[0:99], newyHat1.T))
  print('new yHat10 error Size is :' , rssError(abY[0:99], newyHat10.T))

  standSw = standRegres(abX[0: 99], abY[0: 99])
  standSwHat = mat(abX[100: 199]) * standSw
  print('standRegress error Size is:', rssError(abY[100: 199], standSwHat.T.A))

def rdigeRegres(xMat, yMat, lam=0.2):
  xTx = xMat.T * xMat
  denom = xTx + eye(shape(xMat)[1]) * lam

  if linalg.det(denom) == 0.0:
    print('this matrix can not do inverse')
    return
  ws = denom.I * (xMat.T * yMat)
  return ws

def rdigeRegresTest(xArr, yArr):
  xMat = mat(xArr)
  yMat = mat(yArr).T
  yMean = mean(yMat, 0)
  yMat = yMat - yMean
  xMeans = mean(xMat, 0)
  xVar = var(xMat, 0)
  xMat = (xMat - xMeans) / xVar
  numTestPts = 30
  wMat = zeros((numTestPts, shape(xMat)[1]))
  for i in range(numTestPts):
    ws = rdigeRegres(xMat, yMat, exp(i - 10))
    wMat[i, :] = ws.T
  return wMat

def test3():
    abX,abY = loadDataSet('../AiLearning/data/8.Regression/abalone.txt')
    ridgeWeights = rdigeRegresTest(abX, abY)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(ridgeWeights)
    plt.show()

def regularize(xMat):  # 按列进行规范化
    inMat = xMat.copy()
    inMeans = mean(inMat, 0)  # 计算平均值然后减去它
    inVar = var(inMat, 0)  # 计算除以Xi的方差
    inMat = (inMat - inMeans) / inVar
    return inMat

def stageWise(xArr, yArr, eps=0.01, numIt=100):
  xMat = mat(xArr)
  yMat = mat(yArr).T
  yMean = mean(yMat, 0)
  yMat = yMat - yMean
  xMat = regularize(xMat)
  m, n = shape(xMat)
  ws = zeros((n, 1))
  wsTest = ws.copy()
  wsMax = ws.copy()
  returnMat = zeros((numIt, n))

  for i in range(numIt):
    print(ws.T)
    lowestError = inf
    for j in range(n):
      for sign in [-1, 1]:
        wsTest = ws.copy()
        wsTest[j] += eps * sign
        yTest = xMat * wsTest
        rssE = rssError(xMat.A, yTest.A)
        if rssE < lowestError:
          lowestError = rssE
          wsMax = wsTest
    ws = wsMax.copy()
    returnMat[i, :] = ws.T
  return returnMat

def test4():
  xArr, yArr = loadDataSet('../AiLearning/data/8.Regression/abalone.txt')
  print(stageWise(xArr, yArr, 0.01, 200))
  xMat = mat(xArr)
  yMat = mat(yArr).T
  xMat = regularize(xMat)
  yM = mean(yMat,0)
  yMat = yMat - yM
  weights = standRegres(xMat, yMat.T)
  print(weights.T)

test4()