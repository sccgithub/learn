const myRevealingModule = function () {
  let privateVar = 'scc',
      publicVar = 'hello'
  const privateFuncton = function () {
    console.log(privateVar)
  }
  const publicSetName = function (name) {
    privateVar = name
  }
  const publicGetName = function() {
    privateFuncton()
  }

  return {
    setName: publicSetName,
    gteeting: publicVar,
    getName: publicGetName
  }
}()

myRevealingModule.setName('guyskk')
myRevealingModule.getName()

console.log('----------------------------------')
