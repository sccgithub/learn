Function.prototype.implementsFor = function (ParentClassOrObj) { // eslint-disable-line
  if (ParentClassOrObj.constructor === Function) {
    this.prototype = new ParentClassOrObj()
    this.prototype.constructor = this
    this.prototype.parent = ParentClassOrObj.prototype
  } else {
    this.prototype = ParentClassOrObj
    this.prototype.constructor = this
    this.prototype.patent = ParentClassOrObj
  }
  return this
}

const CoffeeOrder = {
  serveCoffee: function (context) {},
  getFlavor: function () {}
}

const CoffeeFlavor = function (newFlavor) {
  let flavor = newFlavor

  if (typeof this.getFlavor === 'function') {
    this.getFlavor = function () {
      return flavor
    }
  }

  if (typeof this.serveCoffee === 'function') {
    this.serveCoffee = function (context) {
      console.log('serving Coffee flavor' + flavor + 'to table number' + context.getTable())
    }
  }
}

CoffeeFlavor.implementsFor(CoffeeOrder)

const CoffContext = function (tableNumber) {
  return {
    getTable: () => tableNumber
  }
}

const CoffeeFlavorFactory = function (flavorName) {
  let flavors = {}

  return {
    getCoffeeFlavor: function (flavorName) {
      let flavor = flavors[flavorName]
      if (flavor === undefined) {
        flavor = new CoffeeFlavor(flavorName)
        flavors[flavorName] = flavor
      }
      return flavor
    },
    getTotalCoffeeFlavorMade: () => Object.keys(flavors).length
  }
}
let testFlyweight = function () {
  let flavors = new CoffeeFlavor()
  let tables = new CoffContext()
  let ordersMade = 0
  let flavorFactory

  let takeOrders = function (flavorIn, table) {
    flavors[ordersMade] = flavorFactory.getCoffeeFlavor(flavorIn)
    tables[ordersMade++] = new CoffContext(table)
  }

  flavorFactory = new CoffeeFlavorFactory()

  takeOrders('cap', 2)
  takeOrders('cap', 4)
  takeOrders('cap', 4)
  takeOrders('ert', 2)
  takeOrders('cap', 2)
  takeOrders('sdf', 45)
  takeOrders('oip', 22)
  takeOrders('capasca', 32)
  takeOrders('casdwep', 245)

  for (var i = ordersMade.length - 1; i >= 0; i--) {
    flavors.serveCoffee(tables[i])
  }
  console.log()
  console.log('tatal made' + flavorFactory.getTotalCoffeeFlavorMade())
}

testFlyweight()
