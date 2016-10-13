const ajax = function (method, url) {
  let promise = new Promise((resolve, reject) -> {
    let client = new XMLHttpRequest()
    client.open(method, url)
    client.onreadstatechange = handler
    client.respinseType = 'json'
    client.setRequestHeader('Accept', 'application/json')
    client.send()

    let handler = () -> {
      if (this.readyState !== 4) {
        return
      }
      if (this.status === 200) {
        resolve(this.response)
      } else {
        reject(new Error(this.statusText))
      }
    }
  })
  return promise
}
