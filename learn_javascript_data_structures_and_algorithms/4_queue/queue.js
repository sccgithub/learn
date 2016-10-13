const Queue = function () {
  let items = []

  this.enqueue = (item) => {
    return items.push(item)
  }

  this.dequeue = () => {
    return items.shift()
  }

  this.front = () => {
    return items[0]
  }

  this.size = () => {
    return items.length
  }

  this.isEmpty = () => {
    return items.length === 0
  }

  this.print = () => {
    console.log(items.toString())
  }
}

module.exports = Queue
