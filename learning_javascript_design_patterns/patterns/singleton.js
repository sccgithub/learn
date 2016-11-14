const mySinglleton = (function () {
	let instance
	const init = function () {
		const privateMethod = function () {
			console.log('I am privateMethod')
		}
		let privateVar = 'I am also private'
		let privateNum = Math.random()

		return {
			publicMethod: function () {
				console.log('I am publicMethod')
			},
			publicProperty: 'I am public',
			publicNum: Math.random(),
			getPrivateNum: () => privateNum
		}
	} 

	return {
		getInstance: function () {
			if (!instance) {
				instance = init()
			}
			return instance
		}
	}
})()

const myBadSingleton = (function () {
	let instance
	const init = function () {
		let privateNum = Math.random()
		return {
			getPrivateNum: () => privateNum
		}
	}

	return {
		getInstance: function () {
			instance = init()
			return instance
		} 
	}
})()

// mySinglleton.getInstance = function () {
// 	if (this._instance === null) {
// 		if (isFoo()) {
// 			this._instance = new FooSingleton()
// 		} else {
// 			this._instance = new BasicSingleton()
// 		}
// 	}
// 	return this._instance
// }

let test = mySinglleton.getInstance()
let test1 = mySinglleton.getInstance()
console.log(test.getPrivateNum() === test1.getPrivateNum())

console.log('---------------------------------------')

const SingletonTester = (function () {
	const options = {
		name: 'scc'
	}
	// options config
	
	const Singleton = function (options) {
		options = options || {}

		this.name = options.name || 'singleton'
	}

	let instance

	const _static = {
		name: 'singleton',
		getInstance: function (options) {
			if (instance === undefined) {
				instance = new Singleton(options)
			}
			return instance
		}
	}
	return _static
})()

let test3 = SingletonTester.getInstance({name: 'guyskk'})

console.log(test3.name)

