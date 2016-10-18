// 线性探查
const HashTable = function () {
  let table = []

  const loseloseHashCode = (key) => {
    let hash = 5381
    for (var i = 0; i < key.length; i++) {
      hash = hash * 33 + key.charCodeAt(i)
    }
    return hash % 1013
  }

  const ValuePair = function (key, value) {5
    this.key = key
    this.value = value
    this.toString = () => `[${this.key}-${this.value}]`
  }

  this.put = (key, value) => {
    let position = loseloseHashCode(key)
    if (table[position] === undefined) {
      table[position] = new ValuePair(key, value)
    } else {
      let index = ++position
      while (table[index] !== undefined) {
        index++
      }
      table[position] = new ValuePair(key, value)
    }
  }
  this.remove = (key) => {
    let position = loseloseHashCode(key)
    if (table[position] !== undefined) {
      if (table[position].key === key) {
        table[position] = undefined
        return true
      } else {
        let index = ++position
        while (table[index].key !== key) {
          index++
        }
        if (table[index].key === key) {
          return table[index] = undefined
          return true
        }
      }
    }
    return false
  }
  this.get = (key) => {
    let position = loseloseHashCode(key)
    if (table[position] !== undefined) {
      if (table[position].key === key) {
        return table[position].value
      } else {
        let index = ++position
        while (table[index].key !== key) {
          index++
        }
        if (table[index].key === key) {
          return table[index].value
        }
      }
    }
    return undefined
  }
  this.print = () => {
    for (var i = 0; i < table.length; i++) {
      if (table[i] !== undefined) {
        console.log(`${i}:${table[i]}`)
      }
    }
  }
}

let hash = new HashTable()
hash.put('sss', 'wwwww')
hash.put('sss', 'wwwww3')
hash.put('sss', 'wwwww4')
console.log(hash.get('sss'))
console.log(hash.remove('sss'))
