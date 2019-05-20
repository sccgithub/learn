from numpy import *

def loadDataSet(filename):
  dataMat = []
  fr = open(filename)
  for line in fr.readlines():
    curLine = line.strip().split('\t')
    fltLine = list(map(float, curLine))
    dataMat.append(fltLine)
  return dataMat

def distEcloud(vecA, vecB):
  return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataSet, k):
  n = shape(dataSet)[1]
  centroids = mat(zeros((k, n)))
  # 为每一列生成k个随机质心
  for j in range(n):
    minJ = min(dataSet[:, j])
    rangeJ = float(max(dataSet[:, j]) - minJ)
    centroids[:, j] = mat(minJ + rangeJ * random.rand(k, 1))
  return centroids

def KMeans(dataSet, k, distMeas=distEcloud, createCent=randCent):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m, 2))) #存储每行的最小结果
  centroids = createCent(dataSet, k)
  clusterChanged = True

  while clusterChanged:
    clusterChanged = False
    for i in range(m):
      minDist = inf
      minIndex = -1
      for j in range(k):
        distJI = distMeas(centroids[j, :], dataSet[i, :]) # 计算本行数据与k个随机质心的距离
        if distJI < minDist:
          minDist = distJI
          minIndex = j
      if clusterAssment[i, 0] != minIndex: # 更新最小值记录
        clusterChanged = True
        clusterAssment[i, :] = minIndex, minDist ** 2
    print(centroids)
    for cent in range(k):
      # 求出每一族中所有的点
      ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cent)[0]]
      # 将质心修改为簇中所有点的平均值
      centroids[cent, :] = mean(ptsInClust, axis=0)
  return centroids, clusterAssment

def test():
  dataMat = mat(loadDataSet('../AiLearning/data/10.KMeans/testSet.txt'))
  centroids, clusterAssment = KMeans(dataMat, 4)
  # print('-----')
  # print(centroids)
  # print(clusterAssment)

def biKmeans(dataSet, k, distMeas=distEcloud):
  m = shape(dataSet)[0]
  clusterAssment = mat(zeros((m, 2)))
  centroid0 = mean(dataSet, axis=0).tolist()[0]
  centList = [centroid0]
  for j in range(m):
    clusterAssment[j, 1] = distMeas(mat(centroid0), dataSet[j, :]) ** 2
  while len(centList) < k:
    lowestSSE = inf
    for i in range(len(centList)):
      ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A==i)[0],:]
      centroidMat, splitClustAss = KMeans(ptsInCurrCluster, 2, distMeas)
      # 将二分 kMeans 结果中的平方和的距离进行求和
      sseSplit = sum(splitClustAss[:,1])
      # 将未参与二分 kMeans 分配结果中的平方和的距离进行求和
      sseNoSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0], 1])
      if (sseSplit + sseNoSplit) < lowestSSE:
        lowestSSE = sseSplit + sseNoSplit
        bestCentToSplit = i
        bestNewCents = centroidMat
        bestClustAss = splitClustAss.copy()
    bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
    bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
    print('the bestCentToSplit is: ',bestCentToSplit)
    centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]
    centList.append(bestNewCents[1,:].tolist()[0])
    clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss
  return mat(centList), clusterAssment

def test2():
  dataMat = mat(loadDataSet('../AiLearning/data/10.KMeans/testSet2.txt'))
  centList, assment = biKmeans(dataMat, 3)
  print(centList)

test2()