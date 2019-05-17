from numpy import *

def loadDataSet(filename):
  dataMat = []
  fr = open(filename)
  for line in fr.readlines():
    curLine = line.strip().split('\t')
    fltLine = list(map(float, curLine))
    dataMat.append(fltLine)
  return dataMat

def binSplitDataSet(dataSet, feature, value):
  # feature 待切分的特征列
  # value 特征列要比较的值
  mat0 = dataSet[nonzero(dataSet[:, feature] <= value)[0], :]
  mat1 = dataSet[nonzero(dataSet[:, feature] > value)[0], :]
  return mat0, mat1

def regLeaf(dataSet):
  return mean(dataSet[:, -1])

def regErr(dataSet):
  return var(dataSet[:, -1]) * shape(dataSet)[0]

def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
  # 终止条件：最小误差
  tolS = ops[0]
  # 终止条件：最小切割数据条数
  tolN = ops[1]
  if len(set(dataSet[:, -1].T.tolist()[0])) == 1:
    return None, leafType(dataSet)
  
  m, n = shape(dataSet)
  S = errType(dataSet)
  bestS = inf
  bestIndex = 0
  bestValue = 0

  for featIndex in range(n - 1):
    for splitVal in set(dataSet[:, featIndex].T.tolist()[0]):
      mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
      if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
        continue
      newS = errType(mat0) + errType(mat1)
      if newS < bestS:
        bestS = newS
        bestIndex = featIndex
        bestValue = splitVal
  if S - bestS < tolS:
    return None, leafType(dataSet)
  mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
  if shape(mat0)[0] < tolN or shape(mat1)[0] < tolN:
    return None, leafType(dataSet)
  return bestIndex, bestValue


def createTree(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
  feat, val = chooseBestSplit(dataSet, leafType, errType, ops)
  if feat is None:
    return val
  retTree = {}
  retTree['spInd'] = feat
  retTree['spVal'] = val

  lSet, rSet = binSplitDataSet(dataSet, feat, val)
  retTree['left'] = createTree(lSet, leafType, errType, ops)
  retTree['right'] = createTree(rSet, leafType, errType, ops)
  return retTree

def test():
  myDat = loadDataSet('../AiLearning/data/9.RegTrees/data3.txt')
  regTree = createTree(mat(myDat), ops=(1000, 4))
  print(regTree)

def isTerr(obj):
  return (type(obj).__name__ == 'dict')

def getMean(tree):
  if isTerr(tree['left']):
    tree['left'] = getMean(tree['left'])
  if isTerr(tree['right']):
    tree['right'] = getMean(tree['right'])
  return (tree['left'] + tree['right']) / 2

def prune(tree, testData):
  if shape(testData)[0] == 0:
    return getMean(tree)
  
  if isTerr(tree['left']) or isTerr(tree['right']):
    lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
  
  if isTerr(tree['left']):
    tree['left'] = prune(tree['left'], lSet)

  if isTerr(tree['right']):
    tree['right'] = prune(tree['right'], rSet)

  if not isTerr(tree['left']) and not isTerr(tree['right']):
    lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
    errNoMerge = sum(power(lSet[:, -1] - tree['left'], 2)) + sum(power(rSet[:, -1] - tree['right'], 2))
    treeMean = (tree['left'] + tree['right']) / 2
    errMerge = sum(power(testData[:, -1] - treeMean, 2))
    if errNoMerge > errMerge:
      print('merge')
      return treeMean
    else:
      return tree
  else:
    return tree

def test2():
  myDat = loadDataSet('../AiLearning/data/9.RegTrees/data3.txt')
  regTree = createTree(mat(myDat), ops=(2, 5))
  myDatTest = loadDataSet('../AiLearning/data/9.RegTrees/data3test.txt')
  tree = prune(regTree, mat(myDatTest))
  print('----------')
  print('----------')
  print('----------')
  print(tree)

def linearSolve(dataSet):
  m, n = shape(dataSet)

  X = mat(ones((m, n)))
  Y = mat(ones((m, 1)))

  X[:, 1: n] = dataSet[:, 0: n-1]
  Y = dataSet[:, -1]
  xTx = X.T * X
  if linalg.det(xTx) == 0:
    print('This matrix is singular')
  ws = xTx.T * (X.T * Y)
  return ws, X, Y

def modelLeaf(dataSet):
  ws, X, Y = linearSolve(dataSet)
  return ws

def modelErr(dataSet):
  ws, X, Y = linearSolve(dataSet)
  yHat = X * ws
  return sum(power(Y - yHat, 2))

def test3():
  myDat = loadDataSet('../AiLearning/data/9.RegTrees/data3.txt')
  regTree = createTree(mat(myDat), modelLeaf, modelErr, ops=(1, 10))
  # myDatTest = loadDataSet('../AiLearning/data/9.RegTrees/data3test.txt')
  # tree = prune(regTree, mat(myDatTest))
  print('----------')
  print(regTree)

def regTerrEval(model, inDat):
  # print(model)
  return float(model)

def modelTreeEval(model, inDat):
  n = shape(inDat)[1]
  X = mat(ones((n, n+1)))
  X[:, 1: n+1] = inDat
  return X * model

def treeForeCast(tree, inDat, modelEval=regTerrEval):
  if not isTerr(tree):
    return modelEval(tree, inDat)
  if inDat[tree['spInd']] <= tree['spVal']:
    if isTerr(tree['left']):
      return treeForeCast(tree['left'], inDat, modelEval)
    else:
      return modelEval(tree['left'], inDat)
  else:
    if isTerr(tree['right']):
      return treeForeCast(tree['right'], inDat, modelEval)
    else:
      return modelEval(tree['right'], inDat)
  
def createForeCast(tree, testData, modelEval=regTerrEval):
  m = len(testData)
  yHat = mat(ones((m, 1)))
  for i in range(m):
    yHat[i, 0] = treeForeCast(tree, mat(testData[i]), modelEval)
  return yHat


def test4():
  trainMat = mat(loadDataSet('../AiLearning/data/9.RegTrees/bikeSpeedVsIq_train.txt'))
  testMat = mat(loadDataSet('../AiLearning/data/9.RegTrees/bikeSpeedVsIq_test.txt'))
  regTree = createTree(trainMat, ops=(1, 20))
  yHat = createForeCast(regTree, testMat[:, 0])
  print('----------')
  print(corrcoef(yHat, testMat[:, 1], rowvar=0)[0, 1])
  print('----------')
  modelTree = createTree(trainMat, modelLeaf, modelErr, (1, 20))
  yHat = createForeCast(modelTree, testMat[:, 0], modelTreeEval)
  print(corrcoef(yHat, testMat[:, 1], rowvar=0)[0, 1])


test4()
