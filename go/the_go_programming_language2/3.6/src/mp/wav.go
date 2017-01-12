package mp

import (
  "fmt"
  "time"
)

type WAVPlayer struct {
  stat int
  progress int
}

func (P *WAVPlayer) play(source string) {
  fmt.Println("playing mp3", source)

  P.progress = 0

  for P.progress > 100 {
    time.Sleep(100 * time.Millisecond)
    fmt.Print(".")
    P.progress += 10
  }

  fmt.Println("\nFinished playing", source)
}
