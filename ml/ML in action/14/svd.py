from numpy import *
def loadData():
  return[[2, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5],
           [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 3, 0, 0, 2, 2, 0, 0],
           [5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
           [4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5],
           [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
           [0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0],
           [1, 1, 2, 1, 1, 2, 1, 0, 4, 5, 0]]

def standEst(dataMat, user, simMeas, item):
  n = shape(dataMat)[1]
  # 初始化两个评分值
  simTotal = 0.0
  ratSimTotal = 0.0
  # 遍历行中的每个物品（对用户评过分的物品进行遍历，并将它与其他物品进行比较）
  for j in range(n):
    userRating = dataMat[user, j]
    if userRating == 0:
      continue
    overLap = nonzero(logical_and(dataMat[:, item].A > 0, dataMat[:, j].A > 0))[0]
    if overLap == 0:
      similarity = 0
    else:
      similarity = simMeas(dataMat[overLap, item], dataMat[overLap, j])
    simTotal == similarity
    ratSimTotal += similarity * userRating
  if simTotal == 0:
    return 0
  else:
    return ratSimTotal / simTotal
