from numpy import *
from math import log
import feedparser

def loadDataSet():
  postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
  classVec = [0, 1, 0, 1, 0, 1]
  return postingList, classVec

def createVocabList(dataSet):
  vocabSet = set([])
  for document in dataSet:
    vocabSet = vocabSet | set(document)
  return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] = 1
    else:
      print(word, 'is not in vocabList')
  return returnVec

def bagOfWords2Vec(vocabList, inputSet):
  returnVec = [0] * len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] += 1
    else:
      print(word, 'is not in vocabList')
  return returnVec

def trainNB0(trainMatrix, trainCategory):
  numTrainDoc = len(trainMatrix)
  numWords = len(trainMatrix[0])

  pAbusive = sum(trainCategory) / float(numTrainDoc)

  p0num = ones(numWords)
  p1num = ones(numWords)
  p0Denom = 2
  p1Denom = 2
  for i in range(numTrainDoc):
    if trainCategory[i] == 1:
      p1num += trainMatrix[i]
      p1Denom += sum(trainMatrix[i])
    else:
      p0num += trainMatrix[i]
      p0Denom += sum(trainMatrix[i])
  p1vect = [log(pnum / p1Denom) for pnum in p1num]
  p0vect = [log(pnum / p0Denom) for pnum in p0num]
  return p1vect, p0vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
  # 这里的 vec2Classify * p1Vec 的意思就是将每个词与其对应的概率相关联起来
  p1 = sum(vec2Classify * p1Vec) + log(pClass1) # P(w|c1) * P(c1)
  p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1) # P(w|c0) * P(c0)

  if p1 > p0:
    return 1
  else:
    return 0

def testingNB():
  listp, listc = loadDataSet()
  myVocabList = createVocabList(listp)
  trainMat = []

  for pDoc in listp:
    trainMat.append(setOfWords2Vec(myVocabList, pDoc))
  p1v, p0v, pAb = trainNB0(array(trainMat), array(listc))
  testEntry = ['love', 'my', 'dalmation']
  thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
  print(testEntry, 'classified as: ', classifyNB(thisDoc, p0v, p1v, pAb))
  testEntry = ['stupid', 'garbage']
  thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
  print(testEntry, 'classified as: ', classifyNB(thisDoc, p0v, p1v, pAb))

def textParse(bigStr):
  import re
  listOfTokens = re.split(r'\W*', bigStr)
  return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def spamTest():
  docList = []
  classList = []
  fullText = []

  for i in range(1, 26):
    wordList = textParse(open('email/spam/%d.txt' % i, 'r', encoding= u'gbk', errors='ignore').read())
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(1)

    wordList = textParse(open('email/ham/%d.txt' % i, 'r', encoding= u'gbk', errors='ignore').read())
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(0)

  vocabList = createVocabList(docList)
  trainingSet = list(range(50))
  testSet = []
  for i in range(10):
    randIndex = int(random.uniform(0, len(trainingSet)))
    testSet.append(trainingSet[randIndex])
    del(trainingSet[randIndex])
  trainMat = []
  trainClasses = []
  for docIndex in trainingSet:
    trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
    trainClasses.append(classList[docIndex])
  p1v, p0v, pSpam = trainNB0(array(trainMat), array(trainClasses))
  errCount = 0
  for docIndex in testSet:
    wordVector = setOfWords2Vec(vocabList, docList[docIndex])
    if classifyNB(array(wordVector), p0v, p1v, pSpam) != classList[docIndex]:
      errCount += 1
  print('the error rate is :', float(errCount) / len(testSet))

def calcMostFreq(vocabList, fullText):
  import operator
  freqDict = {}
  for token in vocabList:
    freqDict[token] = fullText.count(token)
  sortedFreq = sorted(freqDict.items(), key=operator.itemgetter(1), reverse=True)
  return sortedFreq[:30]

def localWords(feed1, feed0):
  docList = []
  classList = []
  fullText = []
  minLen = min(len(feed1['entries']), len(feed0['entries']))

  for i in range(minLen):
    wordList = textParse(feed1['entries'][i]['summary'])
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(1)

    wordList = textParse(feed0['entries'][i]['summary'])
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(0)

  vocavList = createVocabList(docList)
  top30words = calcMostFreq(vocavList, fullText)

  for pairW in top30words:
    if pairW[0] in vocavList:
      vocavList.remove(pairW[0])

  trainingSet = list(range(2 * minLen))
  testSet = []
  for i in range(20):
    randIndex = int(random.uniform(0, len(trainingSet)))
    testSet.append(trainingSet[randIndex])
    del(trainingSet[randIndex])

  trainMat = []
  trainClasses = []
  for docIndex in trainingSet:
    trainMat.append(bagOfWords2Vec(vocavList, docList[docIndex]))
    trainClasses.append(classList[docIndex])
  p1v, p0v, pSpam = trainNB0(array(trainMat), array(trainClasses))

  errCount = 0
  for docIndex in testSet:
    wordVect = bagOfWords2Vec(vocavList, docList[docIndex])
    if classifyNB(array(wordVect), p0v, p1v, pSpam) != classList[docIndex]:
      errCount += 1
  print('the error rate is ', float(errCount) / len(testSet))
  return vocavList, p0v, p1v

def testLocalWords():
  ny=feedparser.parse('http://newyork.craigslist.org/stp/index.rss')
  sy=feedparser.parse('http://sfbay.craigslist.org/stp/index.rss')

  localWords(ny, sy)

testLocalWords()

# spamTest()

# testingNB()