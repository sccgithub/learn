const assert = require('assert')
const CountStream = require('./1.1.js')
const fs = require('fs')

let countStream = new CountStream('example')
let passed = 0

countStream.on('total', (count) => {
  console.log('count is ' + count)
  assert.equal(count, 1)        
  passed++
})

fs.createReadStream(__filename).pipe(countStream)

process.on('exit', () => {
  console.log('Assertion passed ' + passed)
})
