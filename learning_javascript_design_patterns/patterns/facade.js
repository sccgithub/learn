const mode = (function () {
	let _private = {
		i: 6,
		get: function () {
			console.log('val is ' + this.i)
		},
		set: function (j) {
			console.log(this.i + 'to' + j)
			this.i = j
		},
		run: () => console.log('runing')
	}
	return {
		facade: function (args) {
			_private.set(args.val)
			_private.get()
			if (args.run) {
				_private.run()
			}
		}
	}
})()

mode.facade({val: 3, run: 1})