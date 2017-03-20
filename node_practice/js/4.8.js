const util = require('util')
const domain = require('domain')
const events = require('events')

let audioDomain = domain.create()

function AudioDevice () {
  events.EventEmitter.call(this)
  this.on('play', this.play.bind(this))
}

util.inherits(AudioDevice, events.EventEmitter)

AudioDevice.prototype.play = function () {
  this.emit('error', 'some err')
}

function MusicPlayer () {
  events.EventEmitter.call(this)

  this.audioDevice = new AudioDevice()
  this.on('play', this.play.bind(this))

  this.emit('error', 'no tracks')
}

util.inherits(MusicPlayer, events.EventEmitter)

MusicPlayer.prototype.play = function () {
  this.audioDevice.emit('play')
  console.log('playing')
}

audioDomain.on('error', function (err) {
  console.log('domain', err)
})

audioDomain.run(function () {
  let musicPlayer = new MusicPlayer()
  musicPlayer.play()
})
