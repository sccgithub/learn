/**
 * run
 * use nodemon
 * npm i nodemon -g
 * nodemon 2*.js
 */

// concat
let zero = 0
let positiveNumbers = [1, 2, 3]
let negitiveNumber = [-3, -2, -1]
let number = negitiveNumber.concat(zero, positiveNumbers)
// console.log(number)

/**
* 迭代
*/
const isEven = (x) => {
  console.log(x)
  return (x % 2 === 0) ? true : false
}
let num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]


// every 遇到false就结束
// num.every(isEven)

// some 遇到true就结束
// num.some(isEven)

// forEach 全部迭代
// num.forEach((x) => {
//   console.log(x % 2 === 0)
// })

// map 得到一个存有返回值的新数组
// console.log(num.map(isEven))

// filter 得到一个存有返回值为true的元素新数组
// console.log(num.filter(isEven))

// reduce 四个参数分别为 上次迭代返回值、当前值、当前迭代数、整个数组
// num.reduce((prevReturn, current, index, array) => {
//   console.log(prevReturn, current, index, array)
//   return prevReturn + current
// })

/**
 * 搜索和排序
 */

 // reverse 反序
 // console.log(num.reverse())

 // sort 默认排序，将数字作为字符串进行比较
 // console.log(num.sort())

 // sort 使用自定义函数
 // console.log(num.sort((a, b) => {
 //   return a - b
 // }))
 // 相当于
 // console.log(num.sort((a, b) => {
 //   if (a > b) {
 //     return 1
 //   }
 //   if (b > a) {
 //     return -1
 //   }
 //   return 0
 // }))

 // 自定义排序
 let people = [
   {name: 'lxxyx', age: 33},
   {name: 'scc', age: 11},
   {name: 'island', age: 44},
   {name: 'guskk', age: 22}
 ]
 //
 // console.log(people.sort((a, b) => {
 //   if (a.age > b.age) {
 //     return 1
 //   }
 //   if (b.age > a.age) {
 //     return -1
 //   }
 //   return 0
 // }))

// 字符串排序 默认按首字母ascll码排
let name = ['Alxxy', 'alxxyx', 'Lxxyxx', 'lxxyx']
// console.log(name.sort())
// 忽略大小写
// console.log(name.sort((a, b) => {
//   if (a.toLowerCase() > b.toLowerCase()) {
//     return 1
//   }
//   if (b.toLowerCase() > a.toLowerCase()) {
//     return -1
//   }
//   return 0
// }))

// 搜索
// num.push(10)
// console.log(num.indexOf(10)) // 匹配到的第一个索引
// console.log(num.lastIndexOf(10)) // 匹配到的最后一个索引
// console.log(num.indexOf(100)) // 匹配不到为 -1

/**
 * 数组输出为字符串
 */
 // console.log(num.toString())

 // 加分隔符
 // console.log(num.join('--'))
