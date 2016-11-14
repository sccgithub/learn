(function () {
  let carManage =  {
    requestInfo: function (model, id) {
      console.log('info' + model + id)
    },
    buyCar: function (model, id) {
      console.log('buy car' + model + id)
    },
    arrangeViewing: function (model, id) {
      console.log('book a view' + model + id)
    }
  }
  carManage.execut = function (name) {
    return carManage[name] && carManage[name].apply(carManage, [].slice.call(arguments, 1))
  }
  console.log(carManage.execut('buyCar', 'lxxyx', '12345'))
})()
