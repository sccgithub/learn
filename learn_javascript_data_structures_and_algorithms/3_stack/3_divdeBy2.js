const Stack = require('./3.*')

const divideBy2 = (decNum) => {
  var remStack = new Stack(),
      rem,
      binaryString = ''
  while (decNum > 0) {
    rem = Math.floor(decNum % 2)
    remStack.push(rem)
    decNum = Math.floor(decNum / 2)
    console.log(rem, decNum)
  }

  while (!remStack.isEmpty()) {
    binaryString += remStack.pop().toString()
  }

  return binaryString
}

console.log(divideBy2(22))
