const stringContain = (s1, s2) => {
  s1 = s1.split('').sort()
  s2 = s2.split('').sort()

  for (let pa = 0, pb = 0; pb < s2.length;) {
    while ((pa < s1.length) && (s1[pa] < s2[pb])) {
      ++pa
    }
    if ((pa >= s1.length) || (s1[pa] > s2[pb])) {
      return false
    }
    ++pb
  }
  return true
}

console.log('1: ', stringContain('qwerty', 'qt'))

const stringContain2 = (s1, s2) => {
  let have = {}
  for (let i = 0; i < 26; i++) {
    have[i] = 0
  }

  for (let i = 0; i < s1.length; i++) {
    ++have[s1[i] - 'A']
  }

  for (let i = 0; i < s2.length; i++) {
    if (have[s2[i] - 'A'] === 0) {
      return false
    }
  }
  return true
}

console.log('2: ', stringContain2('qwerty', 'qt'))

const stringContain3 = (s1, s2) => {
  let hash = {}
  for (let i = 0; i < 26; i++) {
    hash[i] = 0
  }
  let m = 0

  for (let i = 0; i < s2.length; i++) {
    let x = s2[i] - 'A'
    if (hash[x] === 0) {
      hash[x] = 1
      ++m
    }
  }
  for (let i = 0; i < s1.length && m > 0; i++) {
    let x = s1[i] - 'A'
    if (hash[x] === 1) {
      --m
      hash[x] = 0
    }
  }
  return m == 0
}

console.log('3: ', stringContain3('qwerty', 'qt'))

const stringContain4 = (s1, s2) => {
  const p = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,61, 67, 71, 73, 79, 83, 89, 97, 101]
  let f = 1
  for (let i = 0; i < s1.length; i++) {
    let x = p[s1[i] - 'A']
    if (f % x) {
      f *= x
    }
  }
  for (let i = 0; i < s2.length; i++) {
    let x = p[s2[i] - 'A']
    if (f % x) {
      return false
    }
  }
  return true
}

console.log('4: ', stringContain4('qwerty', 'qtw'))
