const util = require('util')
const events = require('events')

function MusicPlayer () {
  events.EvevtEmitter.call(this)
}

util.inherits(MusicPlayer, events.EvEntEmitter)
