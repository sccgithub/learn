class treeNode:
  def __init__(self, nameValue, numOccur, parentNode):
    self.name = nameValue
    self.count = numOccur
    self.nodeLink = None
    self.parent = parentNode
    self.children = {}

  def inc(self, numOccur):
    self.count += numOccur
  
  def dosp(self, ind=1):
    for child in self.children.values():
      print(' ' * ind, self.name, ' ', self.count)
      child.disp(ind+1)


def createTree(dataSet, minSup=1):
  headerTable = {}
  for trains in dataSet:
    for item in trains:
      headerTable[item] = headerTable.get(item, 0) + dataSet[trains]
  for k in headerTable.keys():
    if headerTable[k] < minSup:
      del headerTable[k]
  freqItemSet = set(headerTable.keys())
  if len(freqItemSet) == 0:
    return None, None
  for k in headerTable:
    headerTable[k] = [headerTable[k], None]
  retTree = treeNode('null set', 1, None)
  for trainSet, count in dataSet.items():
    localD = {}
    for item in trainSet:
      if item in freqItemSet:
        localD[item] = headerTable[item][0]
    if len(localD) > 0:
      orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
      updateTree(orderedItems, retTree, headerTable, count)
  return retTree, headerTable

# def updateTree(orderedItems, retTree, headerTable, count):