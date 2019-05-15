from numpy import *

def loadSimpleData():
  dataMat = matrix([
    [1., 2.1],
    [2., 1.1],
    [1.3, 1.],
    [1., 1.],
    [2., 1.]
  ])
  classLabels = [1.0, 1.0, -1.0, -1.0, 1.0]

  return dataMat, classLabels

def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):
  retArray = ones((shape(dataMatrix)[0], 1))
  if threshIneq == 'lt':
    retArray[dataMatrix[:, dimen] <= threshVal] = -1.0
  else:
    retArray[dataMatrix[:, dimen] > threshVal] = -1.0
  return retArray

def buildStump(dataArr, classesLabels, D):
  dataMatrix = mat(dataArr)
  labelMat = mat(classesLabels).T
  m, n = shape(dataMatrix)
  numSteps = 10.0
  bestStump = {}
  bestClassEst = mat(zeros((m, 1)))
  minError = inf

  for i in range(n):
    rangeMin = dataMatrix[:, i].min()
    rangeMax = dataMatrix[:, i].max()
    stepSize = (rangeMax - rangeMin) / numSteps
    for j in range(-1, int(numSteps + 1)):
      for inequal in ['lt', 'gt']:
        threshVal = rangeMin + float(j) * stepSize
        predictedVal = stumpClassify(dataMatrix, i, threshVal, inequal)
        errArr = mat(ones((m, 1)))
        errArr[predictedVal == labelMat] = 0
        weightedErr = D.T * errArr

        if weightedErr < minError:
          minError = weightedErr
          bestClassEst = predictedVal.copy()
          bestStump['dim'] = i
          bestStump['thresh'] = threshVal
          bestStump['ineq'] = inequal
  return bestStump, minError, bestClassEst

def loadDataSet(filename):
  numFeat = len(open(filename).readline().split('\t'))
  dataArr = []
  labelArr = []
  fr = open(filename)
  for line in fr.readlines():
    lineArr = []
    curLine = line.strip().split('\t')
    for i in range(numFeat - 1):
      lineArr.append(float(curLine[i]))
    dataArr.append(lineArr)
    labelArr.append(float(curLine[-1]))
  return dataArr, labelArr

def adaBoostTrainDS(dataArr, labelArr, numIt=40):
  weakClassArr = []
  m = shape(dataArr)[0]
  D = mat(ones((m ,1)) / m)
  aggClassEst = mat(zeros((m, 1)))

  for i in range(numIt):
    bestStump, error, bestClassEst = buildStump(dataArr, labelArr, D)
    alpha = float(0.5 * log((1.0 - error / max(error, 1e-16))))
    bestStump['alpha'] = alpha
    weakClassArr.append(bestStump)
    print('alpha=', alpha, 'classEst=', bestClassEst.T, 'bestStump=', bestStump, 'error=', error)
    expon = multiply(-1 * alpha * mat(labelArr).T, bestClassEst)
    print('(-1取反)预测值expon=', expon.T)
    D = multiply(D, exp(expon))
    D = D / D.sum()
    print('当前的分类结果：', alpha * bestClassEst.T)
    aggClassEst += alpha * bestClassEst
    print('叠加后的分类结果aggClassEst: ', aggClassEst.T)
    aggErrors = multiply(sign(aggClassEst) != mat(labelArr).T, ones((m, 1)))
    errorRate = aggErrors.sum() / m
    if errorRate == 0:
      break
  return weakClassArr, aggClassEst

def adaClassify(datToClass, classifierArr):
  dataMat = mat(datToClass)
  m = shape(dataMat)[0]
  aggClassEst = mat(zeros((m, 1)))
  for i in range(len(classifierArr)):
    print(classifierArr[i])
    classEst = stumpClassify(dataMat, classifierArr[i]['dim'],\
      classifierArr[i]['thresh'], classifierArr[i]['ineq'])
    aggClassEst += classifierArr[i]['alpha'] * classEst
  return sign(aggClassEst)

def plotROC(predStrengths, classLabels):
    """plotROC(打印ROC曲线，并计算AUC的面积大小)
    Args:
        predStrengths  最终预测结果的权重值
        classLabels    原始数据的分类结果集
    """
    print('predStrengths=', predStrengths)
    print('classLabels=', classLabels)

    import matplotlib.pyplot as plt
    # variable to calculate AUC
    ySum = 0.0
    # 对正样本的进行求和
    numPosClas = sum(array(classLabels)==1.0)
    # 正样本的概率
    yStep = 1/float(numPosClas)
    # 负样本的概率
    xStep = 1/float(len(classLabels)-numPosClas)
    # argsort函数返回的是数组值从小到大的索引值
    # get sorted index, it's reverse
    sortedIndicies = predStrengths.argsort()
    # 测试结果是否是从小到大排列
    print('sortedIndicies=', sortedIndicies, predStrengths[0, 176], predStrengths.min(), predStrengths[0, 293], predStrengths.max())

    # 开始创建模版对象
    fig = plt.figure()
    fig.clf()
    ax = plt.subplot(111)
    # cursor光标值
    cur = (1.0, 1.0)
    # loop through all the values, drawing a line segment at each point
    for index in sortedIndicies.tolist()[0]:
        if classLabels[index] == 1.0:
            delX = 0
            delY = yStep
        else:
            delX = xStep
            delY = 0
            ySum += cur[1]
        # draw line from cur to (cur[0]-delX, cur[1]-delY)
        # 画点连线 (x1, x2, y1, y2)
        print(cur[0], cur[0]-delX, cur[1], cur[1]-delY)
        ax.plot([cur[0], cur[0]-delX], [cur[1], cur[1]-delY], c='b')
        cur = (cur[0]-delX, cur[1]-delY)
    # 画对角的虚线线
    ax.plot([0, 1], [0, 1], 'b--')
    plt.xlabel('False positive rate')
    plt.ylabel('True positive rate')
    plt.title('ROC curve for AdaBoost horse colic detection system')
    # 设置画图的范围区间 (x1, x2, y1, y2)
    ax.axis([0, 1, 0, 1])
    plt.show()
    '''
    参考说明：http://blog.csdn.net/wenyusuran/article/details/39056013
    为了计算 AUC ，我们需要对多个小矩形的面积进行累加。
    这些小矩形的宽度是xStep，因此可以先对所有矩形的高度进行累加，最后再乘以xStep得到其总面积。
    所有高度的和(ySum)随着x轴的每次移动而渐次增加。
    '''
    print("the Area Under the Curve is: ", ySum*xStep)

def test():
  dataArr, labelArr = loadDataSet('../AiLearning/data/7.AdaBoost/horseColicTraining2.txt')
  weakClassArr, aggClassEst = adaBoostTrainDS(dataArr, labelArr, 40)
  plotROC(aggClassEst.T, labelArr)

  dataArrTest, labelArrTest = loadDataSet('../AiLearning/data/7.AdaBoost/horseColicTest2.txt')
  m = shape(dataArrTest)[0]
  pred10 = adaClassify(dataArrTest, weakClassArr)
  errArr = mat(ones((m, 1)))
  # 测试：计算总样本数，错误样本数，错误率
  print(m, errArr[pred10 != mat(labelArrTest).T].sum(), errArr[pred10 != mat(labelArrTest).T].sum()/m)

test()