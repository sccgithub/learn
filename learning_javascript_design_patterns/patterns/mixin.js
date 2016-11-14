const Person = function (firstName, lastName) {
	this.firstName = firstName
	this.lastName = lastName
	this.gender = 'male'
}

let scc = new Person('s', 'cc')
console.log(scc)

console.log('-----------------------------')

const Superhero = function (firstName, lastName, powers) {
	Person.call(this, firstName, lastName)
	this.powers = powers
}

Superhero.prototype = Object.create(Person.prototype)

let guyskk = new Superhero('guy', 'skk', ['run', 'cook'])
console.log(guyskk)

console.log('----------------------------------')

const myMixins = {
	moveUp: () => console.log('move up'),
	moveDown: () => console.log('move down'),
	stop: () => console.log('stop')
}

const carAnimator = function () {
	this.moveLeft = () => console.log('move left')
}

const extend = function (obj, mixin){
	for (key in mixin) {
		obj.prototype[key] = mixin[key]
	}
}

extend(carAnimator, myMixins)
let test = new carAnimator()
test.stop()
test.moveDown()
test.moveUp()

console.log('-----------------------------------------')

const Car =  function (settings) {
	this.model = settings.model || 'no model'
	this.color = settings.model || 'no color'
}

const Mixin = function () {}

Mixin.prototype = {
	driveForward: () => console.log('driveForward'),
	driveSideWays: () => console.log('driveSideWays'),
	driveBackWard: () => console.log('driveBackWard')
}

const augment = function (receivingClass, givingClass) {
	if (arguments[2]) {
		for (let i = 2, len = arguments.length; i < len; i++) {
			receivingClass.prototype[arguments[i]] = givingClass.prototype[arguments[i]]
		}
	} else {
		for (let method in givingClass.prototype) {
			if (!OBject.hasOwnProperty(receivingClass.prototype, method)) {
				receivingClass.prototype[method] = givingClass.prototype[method]
			}
		}
	}
}

augment(Car, Mixin, 'driveSideWays', 'driveBackWard')

let test3 = new Car({
	color: 'red',
	model: 'new'
})

console.log(test3)
test3.driveBackWard()
test3.driveSideWays()