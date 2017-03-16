const fs = require('fs')

fs.readFile('./3.world.dbf', (er, buf) => {
  let header = {}

  let date = new Date()
  date.setUTCFullYear(1900 + buf[1])
  date.setUTCMonth(buf[2])
  date.setUTCDate(buf[3])
  header.lastUpdate = date.toUTCString()
  header.totalRecords = buf.readUInt32LE(4)
  header.bytesInHeader = buf.readUInt16LE(8)
  header.bytesPreRecord = buf.readUInt16LE(10)

  let files = []
  let fileOffset = 32
  const FILED_TYPES = {
    C: 'Character',
    N: 'Numeric'
  }
  const fileTerminator = 0x0D

  while (buf[fileOffset] !== fileTerminator) {
    let filedBuf = buf.slice(fileOffset, fileOffset + 32)
    let filed = {}

    filed.name = filedBuf.toString('ascii', 0, 11).replace(/\u0000/g, '')
    filed.type = FILED_TYPES[filedBuf.toString('ascii', 11, 12)]
    filed.length = filedBuf[16]
    files.push(filed)

    fileOffset += 32
  }

  let startingRecordOffset = header.bytesInHeader
  let records = []
  for (let i = 0; i < header.totalRecords; i++) {
    let recordOffset = startingRecordOffset + (i + header.bytesPreRecord)
    let record = {}
    record._isDel = buf.readUInt8(recordOffset) === 0x2A
    recordOffset++

    for (let j = 0; j < files.length; j++) {
    }

    for (let j = 0; j < files.length; j++) {
      let filed = files[j]
      let Type = filed.type === 'Numeric' ? Number : String
      record[filed.name] = Type(buf.toString('utf8', recordOffset, recordOffset + filed.length).trim())

      recordOffset += filed.length
    }

    records.push(record)
  }

  console.log({header, files, records})
})
