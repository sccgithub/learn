const CountStream = require('./1.1.js')
const http = require('http')
let countStream = new CountStream('baidu')

http.get('http://www.baidu.com', (res) => {
  res.pipe(countStream)
})

countStream.on('total', (count) => {
  console.log('count is' + count)
})
