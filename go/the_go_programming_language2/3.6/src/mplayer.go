package main

import (
  "fmt"
  "bufio"
  "os"
  "strconv"
  "strings"

  "mlib"
  "mp"
)

var lib *mlib.MusicManager
var id int = 1
var ctrl, signal chan int

func handleLibCommands(tokens []string) {
  switch tokens[1] {
  case "list":
    for i := 0; i < lib.Len(); i++ {
      e, _ := lib.Get(i)
      fmt.Println(i + 1, ":", e.Name, e.Artist, e.Source, e.Type)
    }
  case "add":
    if len(tokens) == 6 {
      id++
      lib.Add(&mlib.MusicEntry{strconv.Itoa(id), tokens[2], tokens[3],
      tokens[4], tokens[5]})
    } else {
      fmt.Println("need <name><artist><source><type>")
    }
  case "remove":
    if len(tokens) == 3 {
      lib.RemoveByName(tokens[2])
    } else {
      fmt.Println("remove need <name>")
    }
  default:
    fmt.Println("un know command", tokens[1])
  }
}

func handlePlayCommands(tokens []string) {
  if len(tokens) != 2 {
    fmt.Println("use play <name>")
    return
  }

  e := lib.Find(tokens[1])
  if e == nil {
    fmt.Println("the music", tokens[1], "does not exist")
    return
  }

  mp.Play(e.Source, e.Type)
}

func main()  {
  fmt.Println(`
    enter fllowing commands contral the player:
    lib list -- view the music list
    lib add <name><artist><<source><type> -- add music
    lib remove <name> -- remove a music
    play name -- play a music
  `)

  lib = mlib.NewMusicManager()

  r := bufio.NewReader(os.Stdin)

  for {
    fmt.Print("enter command -->")

    rawLine, _, _ := r.ReadLine()
    line := string(rawLine)

    if line == "q" || line == "e" {
      break
    }

    tokens := strings.Split(line, " ")

    if tokens[0] == "lib" {
      handleLibCommands(tokens)
    } else if tokens[0] == "play" {
      handlePlayCommands(tokens)
    } else {
      fmt.Println("unkonw command")
    }
  }
}
