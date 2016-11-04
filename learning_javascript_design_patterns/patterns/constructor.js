let obj = new Object()
Object.defineProperty(obj, 'method', {
  value: function () {
    console.log('==__==')
  },
  writable: true
})

obj.method()

// const Car = function (model, year, miles) {
//   this.year = year
//   this.model = model
//   this.miles = miles
//
//   this.toString = () => {
//     return `${this.model} has done ${this.miles}miles in ${this.year}years`
//   }
// }

// 改进
const Car = function (model, year, miles) {
  this.year = year
  this.model = model
  this.miles = miles
}
Car.prototype.toString = function () {
  return `${this.model} has done ${this.miles}miles in ${this.year}years`
}

let myCar = new Car('scc', 124, 345)
console.log(myCar.toString())
