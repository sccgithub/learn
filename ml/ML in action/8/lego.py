from regression import rdigeRegresTest
from numpy import *
from bs4 import BeautifulSoup

def scrapePage(retX, retY, inFile, yr, numPce, origPrc):
  fr = open(inFile)
  soup = BeautifulSoup(fr.read())
  i = 1
  currentRow = soup.findAll('table', r='%d' % i)
  while len(currentRow) != 0:
    currentRow = soup.findAll('table', r='%d' % i)
    title = currentRow[0].findAll('a')[1].text
    lwrTitle = title.lower()
    if (lwrTitle.find('new') > -1) or (lwrTitle.find('nisb') > -1):
      newFlag = 1.0
    else:
      newFlag = 0.0
    soldUnicde = currentRow[0].findAll('td')[3].findAll('span')
    if len(soldUnicde) == 0:
      print('item not sell: ', i)
    else:
      soldPrise = currentRow[0].findAll('td')[4]
      priceStr = soldPrise.text
      priceStr = priceStr.replace('$', '')
      priceStr = priceStr.replace(',', '')
      if len(soldPrise) > 1:
        priceStr = priceStr.replace('Free shipping', '')
      sellingPrice = float(priceStr)
      if sellingPrice > origPrc * 0.5:
        retX.append([yr, numPce, newFlag, origPrc])
        retY.append(sellingPrice)
    i += 1
    currentRow = soup.findAll('table', r='%d' % i)

def setDataCollect(retX, retY):
  scrapePage(retX, retY, '../AiLearning/data/8.Regression/setHtml/lego8288.html', 2006, 800, 49.99)
  scrapePage(retX, retY, '../AiLearning/data/8.Regression/setHtml/lego10030.html', 2002, 3096, 269.99)
  scrapePage(retX, retY, '../AiLearning/data/8.Regression/setHtml/lego10179.html', 2007, 5195, 499.99)
  scrapePage(retX, retY, '../AiLearning/data/8.Regression/setHtml/lego10181.html', 2007, 3428, 199.99)
  scrapePage(retX, retY, '../AiLearning/data/8.Regression/setHtml/lego10189.html', 2008, 5922, 299.99)
  scrapePage(retX, retY, '../AiLearning/data/8.Regression/setHtml/lego10196.html', 2009, 3263, 249.99)

def crossValidation(xArr, yArr, numVal=10):
  m = len(yArr)
  preTrain = 0.9
  indexList = list(range(m))
  errorMat = zeros((numVal, 30))

  for i in range(numVal):
    trainX = []
    trainY = []
    testX = []
    testY = []
    random.shuffle(indexList)
    for j in range(m):
      if j < m * preTrain:
        trainX.append(xArr[indexList[j]])
        trainY.append(yArr[indexList[j]])
      else:
        testX.append(xArr[indexList[j]])
        testY.append(yArr[indexList[j]])
    # 预测
    wMat = rdigeRegresTest(trainX, trainY)

    for k in range(30):
      matTestX = mat(testX)
      matTrainX = mat(trainX)
      # 对数据进行标准化
      meanTrain = mean(trainX, 0)
      varTrain = var(matTrainX, 0)
      matTestX= (matTestX - meanTrain) / varTrain

      # 生成预测结果
      yEst = matTestX * mat(wMat[k, :]).T + mean(trainY)
      # 计算误差
      errorMat[i, k] = ((yEst.T.A - array(testY)) ** 2).sum()
  meanErr = mean(errorMat, 0)
  minMean = float(min(meanErr))
  bestWeight = wMat[nonzero(minMean == meanErr)]

  xMat = mat(xArr)
  yMat = mat(yArr).T
  meanX = mean(xMat,0)
  varX = var(xMat,0)
  unReg = bestWeight / varX
  print('the best model from Ridge Regression is:', unReg)
  print('with constant term: ', -1 * sum(multiply(meanX, unReg)) + mean(yMat))


def test5():
  lgX = []
  lgY = []
  setDataCollect(lgX, lgY)
  crossValidation(lgX, lgY, 10)

test5()
