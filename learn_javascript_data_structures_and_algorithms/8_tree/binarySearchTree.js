const BinarySearchTree = function () {
  const Node = function (key) {
    this.key = key
    this.left = null
    this.right = null
  }

  let root = null

  this.insert = (key) => {
    let newNode = new Node(key)
    const insertNode = (node, newNode) => {
      if (newNode.key < node.key) {
        if (node.left === null) {
          node.left = newNode
        } else {
          insertNode(node.left, newNode)
        }
      } else {
        if (node.right === null) {
          node.right = newNode
        } else {
          insertNode(node.right, newNode)
        }
      }
    }
    if (root === null) {
      root = newNode
    } else {
      insertNode(root, newNode)
    }
    // console.log(root)
  }
  this.search = (key) => {
    const searchNode = (node, key) => {
      if (node === null) {
        return false
      }
      if (key < node.key) {
        return searchNode(node.left, key)
      } else if (key > node.key) {
        return searchNode(node.right, key)
      } else {
        return true
      }
    }
    return searchNode(root, key)
  }
  this.inOrderTraverse = (callback) => {
    const inOrderTraverseNode = (node, callback) => {
      if (node !== null) {
        inOrderTraverseNode(node.left, callback)
        callback(node.key)
        inOrderTraverseNode(node.right, callback)
      }
    }
    inOrderTraverseNode(root, callback)
  }
  this.preOrderTraverse = (callback) => {
    const preOrderTraverseNode = (node, callback) => {
      if (node !== null) {
        callback(node.key)
        preOrderTraverseNode(node.left, callback)
        preOrderTraverseNode(node.right, callback)
      }
    }
    preOrderTraverseNode(root, callback)
  }
  this.postOrderTraverse = (callback) => {
    const postOrderTraverseNode = (node, callback) => {
      if (node !== null) {
        postOrderTraverseNode(node.left, callback)
        postOrderTraverseNode(node.right, callback)
        callback(node.key)
      }
    }
    postOrderTraverseNode(root, callback)
  }
  this.min = () => {
    const minNode = (node) => {
      if (node) {
        while (node.left) {
          node = node.left
        }
        return node.key
      }
      return null
    }
    return minNode(root)
  }
  this.max = () => {
    const maxNode = (node) => {
      if (node) {
        while (node.right) {
          node = node.right
        }
        return node.key
      }
      return null
    }
    return maxNode(root)
  }
  this.remove = (key) => {
    const removeNode = (node, key) => {
      if (node === null) {
        return node
      }
      if (key < node.key) {
        node.left = removeNode(node.left, key)
        return node
      } else if (key > node.key) {
        node.right = removeNode(node.right, key)
        return node
      } else {
        if (node.left === null && node.right === null) {
          node = null
          return node
        }
        if (node.left === null) {
          node = node.right
          return node
        } else if (node.right === null) {
          node = node.left
          return node
        }
        let findMinNode = (node) => {
          while (node.left) {
            node = node.left
          }
          return node
        }
        let aux = findMinNode(node.right)
        node.key = aux.key
        node.right = removeNode(node.right, aux.key)
        return node
      }
    }
    root = removeNode(root, key)
  }
}

const print = (key) => {
  console.log(key)
}

let tree = new BinarySearchTree()
tree.insert(4)
tree.insert(2)
tree.insert(5)
tree.insert(1)
tree.insert(3)
tree.insert(6)
tree.insert(7)
// tree.inOrderTraverse(print)
// tree.preOrderTraverse(print)
// tree.postOrderTraverse(print)
console.log(tree.min())
console.log(tree.max())
console.log(tree.search(3))
console.log(tree.remove(4))
console.log(tree.search(4))
