process.stdin.resume()
process.on('SIGHUP', (sig) => {
  console.log('reloading configuration...', sig)
})

process.emit('SIGHUP', 22)

console.log('pid', process.pid)
