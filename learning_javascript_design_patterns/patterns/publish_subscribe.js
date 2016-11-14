let pubsub = {};

(function (q) {
	let topics = {},
			subUid = -1

	q.publish = function (topic, args) {
		if (!topics[topic]) {
			return false
		}
		let subscribes = topics[topic],
				len = subscribes ? subscribes.length : 0

		while (len--) {
			subscribes[len].func(topic, args)
		}

		return this
	}

	q.subscribe = function (topic, func) {
		if (!topics[topic]) {
			topics[topic] = []
		}

		let token = (++subUid).toString()
		topics[topic].push({
			token: token,
			func: func
		})
		return token
	}

	q.unsubscribe = function (token) {
		for (let m in topics) {
			if (topics[m]) {
				for (let i = 0, j = topics[m].length; i < j; i++) {
					if (topics[m][i].token === token) {
						topics[m].splice(i, 1)
						return token
					}
				}
			}
		}
		return this
	}
})(pubsub)

let messageLogger = function (topics, data) {
	console.log('logging:' + topics + ':' + data)
}

let subscription = pubsub.subscribe('msg', messageLogger)
pubsub.publish('msg', 'qqq')

pubsub.unsubscribe(subscription)

pubsub.publish('msg', 'qq')

console.log('-------------------------------------')


const getCurrentTime = () => {
	let date = new Date(),
			m = date.getMonth() + 1
			d = date.getDate()
			y = date.getFullYear()
			t = date.toLocaleTimeString().toLowerCase()

	return (`${m}/${d}/${y} ${t}`)
}

const addGirdRow = function (data) {
	console.log('addGirdRow', data)
}

const updateCounter = function (data) {
	console.log('updateCounter', data, getCurrentTime())
}

const gridUPdate = function (topic, data) {
	if (data !== undefined) {
		addGirdRow(data)
		updateCounter(data)
	}
}

let subscriber = pubsub.subscribe('newDate', gridUPdate)

pubsub.publish('newDate', {name: 'scc'})
pubsub.publish('newDate', {name: 'lxxyx'})
