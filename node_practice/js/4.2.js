const util = require('util')
const events = require('events')

let AudioDevice = {
  play () {
    console.log('play')
  },

  stop () {
    console.log('stop')
  }
}

function MusicPlayer () {
  this.playing = false
  events.EventEmitter.call(this)
}

util.inherits(MusicPlayer, events.EventEmitter)

let musicPlayer = new MusicPlayer()

musicPlayer.on('play', (track) => {
  this.playing = true
  AudioDevice.play(track)
})

musicPlayer.on('stop', () => {
  this.palying = false
  AudioDevice.stop()
})

musicPlayer.emit('play', 'a song')

setTimeout(() => {
  musicPlayer.emit('stop')
}, 2000)
