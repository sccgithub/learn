const LinkList = require('../5_linkedList/linkList')

// 分离链接
const HashTable = function () {
  let table = []

  const loseloseHashCode = (key) => {
    let hash = 0
    for (var i = 0; i < key.length; i++) {
      hash += key.charCodeAt(i)
    }
    return hash % 37
  }

  const ValuePair = function (key, value) {
    this.key = key
    this.value = value
    this.toString = () => `[${this.key}-${this.value}]`
  }

  this.put = (key, value) => {
    let position = loseloseHashCode(key)
    table[position] = new LinkList()
    table[position].append(new ValuePair(key, value))
    console.log(table[position].toString())
  }
  this.remove = (key) => {
    let position = loseloseHashCode(key)
    if (table[position] !== undefined) {
      let current = table[position].getHead()
      while (current.next) {
        if (current.elem.key === key) {
          table[position].remove(current.elem)
          if (table[position].isEmpty()) {
            table[position] = undefined
          }
          return true
        }
        current = current.next
      }
      if (current.elem.key === key) {
        table[position].remove(current.elem)
        if (table[position].isEmpty()) {
          table[position] = undefined
        }
        return true
      }
    }
    return false
  }
  this.get = (key) => {
    let position = loseloseHashCode(key)
    if (table[position] !== undefined) {
      let current = table[position].getHead()
      while (current.next) {
        if (current.elem.key === key) {
          return current.elem.value
        }
        current = current.next
      }
      if (current.elem.key === key) {
        return current.elem.value
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
hash.put('sss1', 'wwwww3')
hash.put('sss2', 'wwwww4')
console.log(hash.get('sss'))
console.log(hash.remove('sss'))
