// const EventEmitter = require('events').EventEmitter
const fs = require('fs')
let content

function readFileIfRequired (cb) {
  if (!content) {
    fs.readFile(__filename, 'utf-8', (err, data) => {
      content = data
      console.log('readFile')
      cb(err, content)
    })
  } else {
    process.nextTick(() => {
      console.log('cached')
      cb(null, content)
    })
  }
}

readFileIfRequired((err, data) => {
  console.log('1.length:', data.length)

  readFileIfRequired((err, data) => {
    console.log('2.length:', data.length)
  })
  console.log('readFile again')
})

console.log('reading file...')
