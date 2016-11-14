const vehicle = function (vehicleType) {
	this.vehicleType = vehicleType || 'car'
	this.model = 'default'
	this.license = '0000-1111'
}

let test1 = new vehicle('bus')
console.log(test1)

console.log('-------------------------------------')

let truck = new vehicle('truck')

truck.setModel = function (model) {
	this.model = model
}

truck.setColor = function (color) {
	this.color = color
}

truck.setModel('old')
truck.setColor('blue')

console.log(truck)

console.log('------------------------------------------')
// need Interface function
// const reminder = new Interface('List', ['summary', 'placeOrder'])
// let properties = {
// 	name: 'remember to buy the milk',
// 	date: '11-10',
// 	actions: {
// 		summary: () => console.log('buy milk'),
// 		placeOrder: () => console.log('Ordering milk')
// 	}
// }

// const Todo = function (config) {
// 	Interface.ensureImplements(config.actions, reminder)
// 	this.name = config.name
// 	this.mthods = config.actions
// }

// let todoItem = Todo(properties)

// console.log(todoItem)
