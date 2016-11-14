package qsort

import "testing"

func TestQuilckSort1(t *testing.T) {
  values := []int{5, 4, 3, 2, 1}
  QuickSort(values)
  if values[0] != 1 || values[1] != 2 || values[2] != 3 || values[3] != 4 || values[4] != 5 {
    t.Error("QuickSort() failed. Got", values, "expected 1 2 3 4 5")
  }
}

func TestQuilckSort2(t *testing.T) {
  values := []int{5, 5, 3, 2, 1}
  QuickSort(values)
  if values[0] != 1 || values[1] != 2 || values[2] != 3 || values[3] != 5 || values[4] != 5 {
    t.Error("QuickSort() failed. Got", values, "expected 1 2 3 5 5")
  }
}

func TestQuilckSort3(t *testing.T) {
  values := []int{5}
  QuickSort(values)
  if values[0] != 5 {
    t.Error("QuickSort() failed. Got", values, "expected 5")
  }
}
