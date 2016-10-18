const Set = function () {
  let items = {}

  this.has = (value) => {
    return items.hasOwnProperty(value)
  }

  this.add = (value) => {
    if (!this.has(value)) {
      items[value] = value
    }
    return true
  }

  this.remove = (value) => {
    if (this.has(value)) {
      delete items[value]
      return true
    }
    return false
  }

  this.clear = () => {
    items = {}
    return true
  }

  this.size = () => {
    return Object.keys(items).length
  }

  this.values = () => {
    return Object.keys(items)
  }

  this.union = (otherSet) => {
    let unionSet = new Set()
    let values = this.values()
    values.forEach((e) => {
      unionSet.add(e)
    })

    values = otherSet.values()
    values.forEach((e) => {
      unionSet.add(e)
    })
    return unionSet
  }

  this.intersection = (otherSet) => {
    let interSer = new Set()
    let values = this.values()
    for (var i = 0; i < values.length; i++) {
      if (!otherSet.has(values[i])) {
        interSer.add(values[i])
      }
    }
    return interSer
  }

  this.subset = (otherSet) => {
    if (this.size() > otherSet.size()) {
      return false
    } else {
      let values = this.values()
      for (var i = 0; i < values.length; i++) {
        if (!otherSet.has(values[i])) {
          return false
        }
      }
      return true
    }
  }
}

let set = new Set()
// set.add(1)
set.add(3)
console.log(set.size())
console.log(set.values())
let newSet = new Set()
newSet.add(5)
newSet.add(3)
console.log(newSet.union(set).values())
console.log(newSet.intersection(set).values())
console.log(set.subset(newSet))
