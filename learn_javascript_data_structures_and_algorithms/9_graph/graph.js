const Dictionary  = require('../7_map_hashTable/map')
const Queue = require('../4_queue/queue')

const Graph = function () {
  let vertics = []
  let adjList = new Dictionary()

  const initializeColor = () => {
    let color = []
    for (var i = 0; i < vertics.length; i++) {
      color[vertics[i]] = 'white'
    }
    return color
  }

  this.addVertex = (v) =>  {
    vertics.push(v)
    adjList.set(v, [])
  }
  this.addEdge = (v, w) => {
    adjList.get(v).push(w)
    adjList.get(w).push(v)
  }
  this.toString = () => {
    let s = ''
    for (var i = 0; i < vertics.length; i++) {
      s += vertics[i] + ' -> '
      let neighbors = adjList.get(vertics[i])
      for (var j = 0; j < neighbors.length; j++) {
        s += neighbors[j] + ' '
      }
      s += '\n'
    }
    return s
  }
  this.bfs = (v) => {
    let color = initializeColor()
        queue = new Queue()
        d = []
        pred = []
    queue.enqueue(v)

    for (var i = 0; i < vertics.length; i++) {
      d[vertics[i]] = 0
      pred[vertics[i]] = null
    }

    while (!queue.isEmpty()) {
      let u = queue.dequeue()
          neighbors = adjList.get(u)
      color[u] = 'grey'
      for (var i = 0; i < neighbors.length; i++) {
        let w = neighbors[i]
        if (color[w] === 'white') {
          color[w] = 'grey'
          d[w] = d[u] + 1
          pred[w] = u
          queue.enqueue(w)
        }
      }
      color[u] = 'black'
    }
    return {
      distances: d,
      predecessors: pred
    }
  }
  this.dfs = (callback) => {
    let color = initializeColor()

    const dfsVisit = (u, color, callback) => {
      color[u] = 'grey'
      if (callback) {
        callback(u)
      }
      let neighbors = adjList.get(u)
      for (var i = 0; i < neighbors.length; i++) {
        if (color[neighbors[i]] === 'white') {
          dfsVisit(neighbors[i], color, callback)
        }
      }
      color[u] = 'black'
    }

    for (var i = 0; i < vertics.length; i++) {
      if (color[vertics[i]] === 'white') {
        dfsVisit(vertics[i], color, callback)
      }
    }
  }

  let time = 0
  this.DFS = () => {
    let color = initializeColor()
        d = []
        f = []
        p = []
    time = 0

    const DFSVisit = (u, color, d, f, p) => {
      console.log('discovered' + u)
      color[u] = 'grey'
      d[u] = ++time
      let neighbors = adjList.get(u)
      for (var i = 0; i < neighbors.length; i++) {
        let w = neighbors[i]
        if (color[w] === 'white') {
          p[w] = u
          DFSVisit(w, color, d, f, p)
        }
      }
      color[u] = 'black'
      f[u] = ++time
      console.log('visited' + u)
    }

    for (var i = 0; i < vertics.length; i++) {
      f[vertics[i]] = 0
      d[vertics[i]] = 0
      p[vertics[i]] = null
    }
    for (var i = 0; i < vertics.length; i++) {
      if (color[vertics[i]] === 'white') {
        DFSVisit(vertics, color, d, f, p)
      }
    }
  }
}

const printNode = (v) => {
  console.log('value=' + v)
}

let graph = new Graph()
graph.addVertex('a')
graph.addVertex('b')
graph.addVertex('c')
graph.addVertex('d')
graph.addVertex('e')
graph.addEdge('a', 'c')
graph.addEdge('a', 'd')
graph.addEdge('a', 'b')
graph.addEdge('e', 'c')
graph.addEdge('e', 'd')
console.log(graph.toString())
console.log(graph.bfs('a'))
graph.dfs(printNode)
