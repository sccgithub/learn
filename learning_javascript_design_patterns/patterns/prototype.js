const myCar = {
	name: 'sccCar',
	drive: function () {
		console.log('I\'m driving')
	},
	painc: () => console.log('painc')
}

let yourCar = Object.create(myCar)

console.log(yourCar.name)

console.log('-----------------------------')

let sheCar = Object.create(myCar, {
	'name': {
		value: 'sheCar',
		enumerable: true
	},
	onwer: {
		value: 'she'
	}
})

console.log(sheCar.onwer)

console.log('----------------------------------')

const vehiclePrototype = {
	init: function (carModel) {
		this.model = carModel
	},
	getModel: function () {
		console.log(this.model)
	}
}

const vehicle = function (model) {
	let F = function () {}
	F.prototype = vehiclePrototype

	let f = new F
	f.init(model)
	return f
}

let car = vehicle('aaaaaaasxsxs')
car.getModel()

console.log('----------------------------------')

let beget = (function () {
	let F = function () {}
	return function (proto) {
		F.prototype = proto
		return new F()
	}
})()

let test11 = beget(vehiclePrototype)
