const ArrayList = function () {
  let array = []

  const swap = (i, j) => {
    let mid = array[i]
    array[i] = array[j]
    array[j] = mid
  }

  this.insert = (item) => {
    array.push(item)
  }

  this.toString = () => {
    return array.join('-')
  }

  this.bubbleSort = () => {
    let length = array.length
    for (let i = 0; i < length; i++) {
      for (var j = 0; j < length - 1 - i; j++) {
        if (array[j] < array[j + 1]) {
          swap(j, j + 1)
        }
      }
    }
  }

  this.selectionSort = () => {
    let length = array.length,
        indexMin
    for (let i = 0; i < length - 1; i++) {
      indexMin = i
      for (let j = i; j < length; j++) {
        if (array[indexMin] > array[j]) {
          indexMin = j
        }
      }
      if (i !== indexMin) {
        swap(indexMin, i)
      }
    }
  }

  this.insertionSort = () => {
    let length = array.length,
        j, temp

    for (let i = 0; i < length; i++) {
      j = i
      temp = array[i]
      while (j > 0 && array[j - 1] > temp) {
        array[j] = array[j - 1]
        j--
      }
      array[j] = temp
    }
  }

  this.mergeSort = () => {
    const merge = (left, right) => {
      let result = []
          il = 0
          ir = 0
      while (il < left.length && ir < right.length) {
        if (left[il] < right[ir]) {
          result.push(left[il++])
        } else {
          result.push(right[ir++])
        }
      }
      while (il < left.length) {
        result.push(left[il++])
      }
      while (ir < right.length) {
        result.push(right[ir++])
      }
      return result
    }
    const mergeSortRec = (array) => {
      let length = array.length
      if (length === 1) {
        return array
      }
      let mid = Math.floor(length / 2),
          left = array.slice(0, mid),
          right = array.slice(mid, length)
      return merge(mergeSortRec(left), mergeSortRec(right))
    }

    array = mergeSortRec(array)
  }

  this.quickSort = () => {
    const swapQuickSort = (array, left, right) => {
      let mid = array[left]
      array[left] = array[right]
      array[right] = mid
    }
    const position = (array, left, right) => {
      let pivot = array[Math.floor((right + left) / 2)],
          i = left,
          j = right
      while (i <= j) {
        while (array[i] < pivot) {
          i++
        }
        while (array[j] > pivot) {
          j--
        }
        if (i <= j) {
          swapQuickSort(array, i, j)
          i++;
          j--
        }
      }
      return i
    }
    const quick = (array, left, right) => {
      let index
      if (array.length > 1) {
        index = position(array, left, right)
        if (left < index - 1) {
          quick(array, left, index - 1)
        }
        if (index < right) {
          quick(array, index, right)
        }
      }
    }
    quick(array, 0, array.length - 1)
  }

  this.binarySearch = (item) => {
    this.quickSort()
    let low = 0,
        high = array.length - 1,
        mid,
        element
    while (low <= high) {
      mid = Math.floor((low + high) / 2)
      element = array[mid]
      if (element < item) {
        low = mid + 1
      } else if (element > item) {
        high = mid - 1
      } else {
        return mid
      }
    }
    return -1
  }
}

let test = new ArrayList()
test.insert(1)
test.insert(12)
test.insert(11)
test.insert(155)
test.insert(123)
test.insert(61)
test.insert(7)
test.insert(47)

// test.bubbleSort()
// test.selectionSort()
// test.insertionSort()
// test.mergeSort()
// test.quickSort()
// console.log(test.binarySearch(11))

console.log(test.toString())
