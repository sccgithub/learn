/**
 * [description]
 * @param  {string} s
 * @param  {number} n
 */
const leftShift = (s, n) => {
  s = Array.from(s)
  while (n--) {
    s.push(s.shift())
  }
  console.log(s.join())
}

leftShift('qwer', 1)

/**
 * the method of 三步反转法
 * @param  {string}
 * @param  {number} n
 */
const leftShift2 = (s, n) => {
  s = Array.from(s)
  let noMove = s.slice(0, n)
  let move = s.slice(n, s.length)
  s = noMove.reverse().concat(move.reverse()).reverse()
  console.log(s.join())
}

leftShift2('qwer', 2)
