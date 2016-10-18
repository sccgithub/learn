const Dictionary = function () {
  let items = {}

  this.set = (key, value) => {
    items[key] = value
  }
  this.remove = (key) => {
    if (this.has(key)) {
      delete items[key]
      return true
    }
    return false
  }
  this.has = (key) => {
    return key in items
  }
  this.get = (key) => {
    return this.has(key) ? items[key] : undefined
  }
  this.clear = () => {
    this.items = {}
  }
  this.size = () => {
    return Object.keys(items).length
  }
  this.keys = () => {
    return Object.keys(items)
  }
  this.values = () => {
    let values = {}
    for (let key in items) {
      if (this.has(key)) {
        values.push(items[key])
      }
    }
    return values
  }
  this.getItems = () => {
    return items
  }
  this.print = () => {
    console.log(items)
  }
}

let map = new Dictionary()
map.set(1,2)
map.print()
// map.print()
// map.print()
// map.print()
// map.print()
// map.print()
// map.print()
// map.print()
