const Queue = require('./queue')

const hotPotato = (nameList, num) => {
  let queue = new Queue()

  nameList.forEach((ele) => {
    queue.enqueue(ele)
  })
  let eliminated = ''
  while (queue.size() > 1) {
    queue.print()
    for (var i = 0; i < num.length; i++) {
      queue.enqueue(queue.dequeue(num[i]))
    }
    console.log(Math.random() < (2 / num))
    if (Math.random() < (2 / num)) {
      eliminated = queue.dequeue()
      console.log(eliminated + '被淘汰')
    }
  }
  return queue.dequeue()
}

let names = [1, 2, 3, 4, 5, 6, 7, 8, 9]
let winner = hotPotato(names, 10)
console.log('winner is' + winner)
