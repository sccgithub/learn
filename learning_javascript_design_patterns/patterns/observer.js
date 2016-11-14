const ObserverList = function () {
	this.observerList = []
}

ObserverList.prototype.Add = function (obj) {
	return this.observerList.push(obj)
}

ObserverList.prototype.Empty = function () {
	this.observerList = []
}

ObserverList.prototype.Count = function () {
	return this.observerList.length
}

ObserverList.prototype.Get = function (index) {
	if (index > -1 && index < this.observerList.length) {
		return this.observerList[index]
	}
}

ObserverList.prototype.Insert = function (obj, index) {
	let pointer = -1
	if (index === 0) {
		this.observerList.unshift(obj)
		pointer = index
	} else if (index = this.observerList.length) {
		this.observerList.push(obj)
		pointer = index
	} else {
		this.observerList
	}
	return pointer
}

ObserverList.prototype.IndexOf = function (obj, startIndex) {
	let i = startIndex,
			pointer = -1

	while (i < this.observerList.length) {
		if (obj === this.observerList[i]) {
			pointer = i
		}
		i++
	}
	return pointer
}

ObserverList.prototype.RemoveIndexAt = function (index) {
	if (index === 0) {
		this.observerList.shift()
	} else if (index === this.observerList.length) {
		this.observerList.pop()
	}
}

const extend = function (obj, extension) {
	for (let key in obj) {
		extension[key] = obj[key]
	}
}

const Subject = function () {
	this.observers = new ObserverList()
}

Subject.prototype.AddObserver = function (observer) {
	this.observers.Add(observer)
}

Subject.prototype.RemoveObsever = function (observer) {
	this.observers.RemoveIndexAt(this.observers.indexOf(observer, 0))
}

Subject.prototype.Notify = function (context) {
	let observerCount = this.observers.Count()
	for (let i = observerCount - 1; i >= 0; i--) {
		this.observers.Get(i).Update(context)
	}
}

const Observer = function () {
	this.Update = function (context) {
		console.log(context)
	}
}


let testaArr = {}
extend(new Subject, testaArr)
const addTestObjToTestAtt = function (obj) {
	extend(new Observer, obj)
	console.log(obj)
	testaArr.AddObserver(obj)
}
let s = {check: 0}
addTestObjToTestAtt(s)
console.log(testaArr.observers)
testaArr.Notify('efe')