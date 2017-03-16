// url
const regexUrl = new RegExp('https?://[-\w.]+(:\d+)?(/([\w/_.]*)?)?')
const testStr = 'https://developer.mozilla.org'
console.log(regexUrl.test(testStr))

// full url
const regexFullUrl = new RegExp('https?://(\w*:\w*@)?[-\w.]+(:\d+)?(/([\w/_/]*(\?\S+)?)?)?')
const testStr2 = 'https://developer.mozilla.org'
console.log(regexFullUrl.test(testStr2))
