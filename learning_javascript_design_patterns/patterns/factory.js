const Car  = function (options) {
	this.doors = options.doors || 4
	this.state = options.state || 'new'
	this.color = options.color || 'black'
}
Car.prototype.drive = true
const Truck = function (options) {
	this.drive = true
	this.state = options.state || 'used'
	this.wheelSize = options.wheelSize || 'large'
	this.color = options.color || 'black'
}

const VehicleFactory = function () {}

VehicleFactory.prototype.vehicleClass = Car

VehicleFactory.prototype.createVehicle = function (options) {
	if (options.vehicleType === 'car') {
		this.vehicleClass = Car
	} else {
		this.vehicleClass = Truck
	}
	return new this.vehicleClass(options)
}

let carFactory = new VehicleFactory()

let car = carFactory.createVehicle({
	vehicleType: 'car',
	color: 'red',
	doors: 6
})

console.log(car)

console.log('------------------------------')

const AbstractVehicleFactory = (function () {
	let types = {}
	return {
		getVehicle: function (type, customizations) {
			let Vehicle = types[type]
			return (Vehicle) ? new Vehicle(customizations) : null
		},
		registerVehicle: function (type, Vehicle) {
			let proto = Vehicle.prototype
			if (proto.drive) {
				types[type] = Vehicle
			}
			return AbstractVehicleFactory
		}
	}
})() 

AbstractVehicleFactory.registerVehicle('car', Car)
AbstractVehicleFactory.registerVehicle('truck', Truck)

let car2 = AbstractVehicleFactory.getVehicle('car', {
	color: 'blue',
	doors: 10
})

console.log(car2)