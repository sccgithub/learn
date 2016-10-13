const LinkedList = function () {
  const Node = function (elem) {
    this.elem = elem
    this.next = null
  }

  let length = 0
  let head = null

  this.append = (elem) => {
    let node = new Node(elem),
        current
    if (head === null) {
      head = node
    } else {
      current = head
      while (current.next) {
        current = current.next
      }
      current.next = node
    }
    length++
    return true
  }
  this.insert = (position, elem) => {
    if (position > -1 && position <= length) {
      let current = head,
          prev,
          index = 0,
          node = new Node(elem)
      if (position === 0) {
        node.next = head
      } else {
        while (index++ < position) {
          prev = current
          current = current.next
        }
        prev.next = node
        node.next = current
        length++
      }
      return true
    } else {
      return false
    }
  }
  this.removeAt = (position) =>{
    if (position > -1 && position < length) {
      let current = head,
          prev,
          index = 0
      if (position === 0) {
        head = current.next
      } else {
        while (index++ < position) {
          prev = current
          current = current.next
        }
        prev.next = current.next
      }
      length--
      return current.elem
    } else {
      return null
    }
  }
  this.remove = (elem) => {
    let index = this.indexOf(elem)
    return this.removeAt(index)
  }
  this.indexOf = (elem) => {
    let current = head,
        index = 0
    while (current) {
      if (current.elem === elem) {
        return index
      }
      current = current.next
      index++
    }
    return -1
  }
  this.isEmpty = () => {
    return length === 0
  }
  this.size = () => {
    return length
  }
  this.toString = () => {
    let current = head,
        string = ''
    while(current) {
      string += current.elem.toString()
      current = current.next
    }
    return string
  }
  this.getHead = () => {
    return head
  }
}

// let list = new LinkedList()
// list.append(22)
// list.append(33)
// list.append(33)
// list.append(33)
// console.log(list.removeAt(1))
// console.log(list.insert(2,333))
// console.log(list.remove(33))
// console.log(list.isEmpty())
// console.log(list.size())
// console.log(list.getHead())
