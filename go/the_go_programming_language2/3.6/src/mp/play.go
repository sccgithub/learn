package mp

import "fmt"

type player interface {
  play(source string)
}

func Play(source, mtype string) {
  var P player

  switch mtype {
  case "MP3":
    P = &MP3Player{}
  case "WAV":
    P = &WAVPlayer{}
  default:
    fmt.Println("un konw type", mtype)
    return
  }

  P.play(source)
}
