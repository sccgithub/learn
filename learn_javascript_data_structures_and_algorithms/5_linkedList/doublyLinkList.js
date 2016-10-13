const DoublyLinkList = function () {
  const Node = function (elem) {
    this.elem = elem
    this.prev = null
    this.next = null
  }

  let length = 0,
      head = null,
      tail = null

  this.insert = (position, elem) => {
    if (position > -1 && position <= length) {
      let node = new Node(elem),
          current = head,
          prev,
          index = 0
      if (position === 0) {
        if (!head) {
          head = node
          tail = node
        } else {
          node.next = current
          head.prev = node
          head = node
        }
      } else if (position === length) {
        current = tail
        current.next = node
        node.prev = current
        tail = node
      } else {
        while (index++ < position) {
          prev = current
          current = current.next
        }
        prev.next = node
        node.next = current
        node.prev = prev
        current.prev = node
      }
      length++
      return true
    } else {
      return false
    }
  }

  this.removeAt = (position) => {
    if (position > -1 && position < length) {
      let current = head,
          prev,
          index = 0

      if (position === 0) {
        head = current.next
        if (length === 1) {
          tail = null
        } else {
          head.prev = null
        }
      } else if (position === length - 1) {
        tail = tail.prev
        tail.next = null
      } else {
        while (index++ < position) {
          prev = current
          current = current.next
        }
        prev.next = current.next
        current.next.prev = prev
      }
      length--
      return current.elem
    } else {
      return false
    }
  }
}

// let list = new DoublyLinkList()
// console.log(list.insert(0, 1))
// console.log(list.insert(1, 2))
// console.log(list.insert(2, 3))
// console.log(list.removeAt(1))
