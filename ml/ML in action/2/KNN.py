
# 导入科学计算包numpy和运算符模块operator
from numpy import *
import operator
from os import listdir
from collections import Counter
# from imp import reload
# import matplotlib
# import matplotlib.pyplot as plt

def file2matrix (fileName):
  """
  Desc:
    import file data
  """
  fr = open(fileName)
  arrayOLines = fr.readlines()
  numberOfLines = len(arrayOLines)

  returnMat = zeros((numberOfLines, 3))
  classLabelVector = []
  index = 0

  for line in arrayOLines:
    line = line.strip()
    listFromLine = line.split('\t')
    returnMat[index, :] = listFromLine[0: 3]
    classLabelVector.append(int(listFromLine[-1]))
    index += 1
  
  return returnMat, classLabelVector
  

def autoNorm(dataSet):
  minVals = dataSet.min(0)
  maxVals = dataSet.max(0)
  ranges = maxVals - minVals
  normoreDataSet = zeros(shape(dataSet))
  m = dataSet.shape[0]
  normoreDataSet = dataSet - tile(minVals, {m, 1})
  normoreDataSet = normoreDataSet / tile(ranges, (m, 1))

  return normoreDataSet, ranges, minVals

def classify0(inX, dataSet, labels, k):
  m = dataSet.shape[0]
  diffMat = tile(inX, (m, 1)) - dataSet
  sqDiffMat = diffMat ** 2
  sqDistances = sqDiffMat.sum(axis=1)
  distance = sqDistances ** 0.5

  sortedDistIndicies = distance.argsort()
  classCount = {}
  for i in range(k):
    voteIlabel = labels[sortedDistIndicies[i]]
    classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
  sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
  # print('sortedClassCount', sortedClassCount)
  return sortedClassCount[0][0]

def datingClassTest():
  hoRotio = 0.1
  datingDataMat, datingLabels = file2matrix('./datingTestSet2.txt')
  normMat, ranges, minVals = autoNorm(datingDataMat)
  m = normMat.shape[0]
  numTestVectors = int(m * hoRotio)
  print('numTestVectors', numTestVectors)
  errCount = 0.0
  for i in range(numTestVectors):
    classifierResult = classify0(normMat[i, :], normMat[numTestVectors:m, :], datingLabels[numTestVectors:m], 3)
    # print('the classifier came back with: ', classifierResult, 'the real answer is: ', datingLabels[i])
    if (classifierResult != datingLabels[i]):
      errCount += 1.0
  print('the total error rate is: ', errCount / float(numTestVectors))

# datingClassTest()

def img2vector(filename):
  returnVect = zeros((1, 1024))
  fr = open(filename)
  for i in range(32):
    linStr = fr.readline()
    for j in range(32):
      returnVect[0, 32 * i + j] = int(linStr[j])
  return returnVect

def handWritingClassTest():
  hwLabels = []
  trainingleList = listdir('./trainingDigits')
  m = len(trainingleList)
  trainingMat = zeros((m, 1024))
  for i in range(m):
    fileNameStr = trainingleList[i]
    fileStr = fileNameStr.split('.')[0]
    classNumStr = int(fileStr.split('_')[0])
    hwLabels.append(classNumStr)
    trainingMat[i, :] = img2vector('./trainingDigits/%s' % fileNameStr)

  testFileList = listdir('./testDigits')
  errorCount = 0.0
  mTest = len(testFileList)
  for i in range(mTest):
      fileNameStr = testFileList[i]
      fileStr = fileNameStr.split('.')[0]
      classNumStr = int(fileStr.split('_')[0])
      vectorUnderTest = img2vector('./testDigits/%s' % fileNameStr)

      classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
      print('the classifier came back with: ', classifierResult, 'the real answer is: ', classNumStr)
      if (classifierResult != classNumStr):
        errorCount += 1.0
  print('the total error rate is: ', errorCount / float(mTest))

# handWritingClassTest()