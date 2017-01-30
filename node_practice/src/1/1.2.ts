import CountStream =require('./1.1')
import http from 'http'

let countStream = new CountStream('baidu')

http.get('http://www.baidu.com', (res) => {
  res.pipe(countStream)
})
