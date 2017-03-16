const EventEmitter = require('events').EventEmitter

function complexOperation () {
  let events = new EventEmitter()
  process.nextTick(() => { // <co id="callout-globals-nexttick-2"/>
    events.emit('success')
  })

  return events
}

complexOperation().on('success', () => {
  console.log('success')
})
