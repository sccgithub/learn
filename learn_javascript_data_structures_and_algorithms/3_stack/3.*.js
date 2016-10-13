/**
 * run
 * use nodemon
 * npm i nodemon -g
 * nodemon 2*.js
 */

const Stack = function () {
  let item = []
  /**
   * @description 添加新元素到栈顶
   * @param el 被添加元素
   * @return 被添加元素
   */
  this.push = (el) => {
    return item.push(el)
  }

  /**
   * @description 移除栈顶元素
   × @return 被移除元素
   */
   this.pop = () => {
     return item.pop()
   }

   /**
    * @description 获取栈顶元素
    * @return 栈顶元素
    */
    this.peek = () => {
      return item[item.length - 1]
    }

  /**
   * @description 判断是否为空
   × @return {boolean} 是否为空
   */
   this.isEmpty = () => {
     return item.length === 0
   }

   /**
    * @description 获取长度
    * @return {number} 栈长度
    */
    this.size = () => {
      return item.length
    }

  /**
   * @description 清空栈
   */
   this.clear = () => {
     item = []
   }

 /**
  * @desc 打印内容
  */
  this.print = () => {
    console.log(item.toString())
  }
}

module.exports = Stack
