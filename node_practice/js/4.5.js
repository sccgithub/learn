const EventEmitter = require('events').EventEmitter

function MusicPlayer (track) {
  this.track = track
  this.playing = false

  for (let methodName in EventEmitter.prototype) {
    this[methodName] = EventEmitter.prototype[methodName]
  }
}

MusicPlayer.prototype = {
  toString: function () {
    if (this.playing) {
      return 'now playing ' + this.track
    }
    return 'stoped'
  }
}

let musicPlayer = new MusicPlayer('a song')

musicPlayer.on('play', function () {
  this.playing = true
  console.log(this.toString())
})

musicPlayer.on('error', (err) => {
  console.error(err)
})

musicPlayer.emit('play')
