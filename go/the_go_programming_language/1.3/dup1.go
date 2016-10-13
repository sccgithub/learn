package main

import (
  "bufio"
  "fmt"
  "os"
)

func main() {
  consts := make(map[string]int)
  input := bufio.NewScanner(os.Stdin)
  for input.Scan() {
    consts[input.Text()]++
    fmt.Println(consts)
    for line, n := range consts {
      if n > 1 {
        fmt.Printf("%d\t%s\n", n, line)
      }
    }
  }
}

// 不知道书原版的意思，运行了没有输出，自己加了输出，
// 改变循环位置，每次输入都会遍历map输出重复项
