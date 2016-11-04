const myModule = {
  myConfig: {
    username: 'scc',
    language: 'zh-cn'
  },
  myMethod: function (newConfig) {
    if (typeof newConfig === 'object') {
      this.myConfig = newConfig
      console.log(this.myConfig.username)
    }
  }
}

myModule.myMethod({
  username: 'guyskk',
  language: 'en'
})

console.log('------------------------------')

const testModule = (function () {
  let counter = 0
  return {
    incermentCounter: function () {
      return ++counter
    },
    resetCounter: function () {
      console.log(counter + 'reset to 0')
      counter = 0
    }
  }
})()

testModule.incermentCounter()
testModule.incermentCounter()
testModule.incermentCounter()
testModule.incermentCounter()
testModule.resetCounter()

console.log('------------------------------')

const myNamespace = (function () {
  let myPrivateVar = 0
  let myPrivateMethod = function (foo) {
    console.log(foo)
  }

  return {
    myPublicVar: 'foo',
    myPublicFunction: function (bar) {
      myPrivateVar++
      myPrivateMethod(bar)
    }
  }
})()

myNamespace.myPublicFunction('myNamespace')

console.log('------------------------------')

const basketModule = (function () {
  let basket = []
  const doSomethingPrivate = function (){
    console.log(basket)
  }

  return {
    addItem: function (item) {
      basket.push(item)
    },
    console: doSomethingPrivate
  }
})()

basketModule.addItem(1)
basketModule.addItem(12)
basketModule.addItem(13)
basketModule.addItem(14)
basketModule.addItem(16)
basketModule.console()

console.log('------------------------------')
