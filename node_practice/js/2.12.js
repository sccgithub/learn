let args = {
  '-h': displayHelp,
  '-r': readFile
}

function displayHelp () {
  console.log('displayHelp')
}

function readFile (file) {
  if (file && file.length) {
    console.log('reading:', file)
    console.time('read')
    let stream = require('fs').createReadStream(file)
    stream.on('end', () => {
      console.timeEnd('read')
    })
    stream.pipe(process.stdout)
  } else {
    console.error('need -r option')
    process.exit(1)
  }
}

if (process.argv.length > 0) {
  args['-r'].apply(this, process.argv.slice(process.argv.length - 1))
}
