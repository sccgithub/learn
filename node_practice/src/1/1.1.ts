import {Writable} from 'stream'

class CountStream extends Writable {
  count: number
  matcher: Object
  constructor (matchText: string, options: any) {
    super(options)
    this.count = 0
    this.matcher = new RegExp(matchText, 'ig')
  }
  _write (chunk, encoding, cb) {
    let matches = chunk.toString().match(this.matcher)
    if (matches) {
      this.count += matches.length
    }
    cb()
  }
  end () {
    this.emit('total', this.count)
  }
}

module.exports = CountStream
