const util = require('util')
const events = require('events')

function Pulsar (speed, times) {
  events.EventEmitter.call(this)

  let self = this
  this.speed = speed
  this.times = times

  this.on('newListener', function (eventName, listener) {
    if (eventName === 'pulse') {
      self.start()
    }
  })
}

util.inherits(Pulsar, events.EventEmitter)

Pulsar.prototype.start = function () {
  let self = this
  let id = setInterval(function () {
    self.emit('pulse')
    self.times--
    if (self.times === 0) {
      clearInterval(id)
    }
  }, this.speed)
}

Pulsar.prototype.stop = function () {
  if (this.listeners('pulse').length === 0) {
    throw new Error('no listener')
  }
}

let pulsar = new Pulsar(500, 5)

// 4.10
pulsar.on('pulse', () => console.log('.'))

// 4.11
pulsar.stop()
