// 归并
const mergeSort = (arr: number[]): number[] => {
  if (arr.length < 2) {
    return arr
  }
  let mid = parseInt(String(arr.length / 2))
  let left = arr.slice(0, mid)
  let right = arr.slice(mid)
  return merge(mergeSort(left), mergeSort(right))
}

const merge = (left: number[], right: number[]): number[] => {
  let result = []
  let i = 0, j = 0
  while (i < left.length && j < right.length) {
    if (left[i] > right[j]) {
      result.push(left[i])
      i++
    } else {
      result.push(right[j])
      j++
    }
  }
  while (i < left.length) {
    result.push(left[i])
    i++
  }
  while (j < right.length) {
    result.push(right[j])
    j++
  }
  return result
}

const testArr = [3,4,5,7,1,9,8,2,0,6]

console.log(mergeSort(testArr))