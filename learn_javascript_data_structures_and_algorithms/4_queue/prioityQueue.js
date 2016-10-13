const PrioityQueue = function () {
  let items = []

  const QueueElement = function (elem, prioity) {
    this.elem = elem
    this.prioity = prioity
  }

  this.enqueue = (elem, prioity) => {
    let queueElement = new QueueElement(elem, prioity)
    if (this.isEmpty()) {
      items.push(queueElement)
    } else {
      let added = false
      for (var i = 0; i < items.length; i++) {
        if (items[i].prioity < prioity) {
          item.splice(i - 1, 0, queueElement)
          added = true
          break
        }
      }
      if (!added) {
        items.push(queueElement)
      }
    }
  }

  this.dequeue = () => {
    return items.shift()
  }

  this.front = () => {
    return items[0]
  }

  this.size = () => {
    return items.length()
  }

  this.isEmpty = () => {
    return items.length === 0
  }

  this.print = () => {
    console.log(items.toString())
  }
  console.log(items)
}

module.exports = PrioityQueue
