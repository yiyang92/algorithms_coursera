from __future__ import print_function
from __future__ import division

import numpy as np
import timeit
import tqdm
from collections import OrderedDict


# Bubble sort and selection sort
class SortArray():
    def __init__(self, array, input_file=None):
        self._arr = array.copy()
        self._input_file = input_file

    @property
    def arr(self):
        return self._arr

    @property
    def input_file(self):
        return self._input_file

    def bubble_sort(self):
        # Define sort first
        def sort():
            swap = False
            for i in range(0, len(self.arr)-1):
                if self.arr[i] > self.arr[i+1]:
                    temp = self.arr[i+1]
                    self.arr[i+1] = self.arr[i]
                    self.arr[i] = temp
                    swap = True
            return swap
        # Do until no need for swap
        swap = True
        while swap == True:
            swap = sort()

    def sel_sort(self):
        min_ind = 0
        for i in range(0, len(self.arr)-1):
            cur_min = self.arr[0]
            # find minimum
            for j in range(i, len(self.arr)):
                # remember index of minimal element
                if j < cur_min:
                    min_ind = j
            # swap if arr[min_ind] < cur_min
            if self.arr[min_ind] < cur_min:
                self.arr[0] = self.arr[min_ind]
                self.arr[min_ind] = cur_min

    def read_array_file(self, test_corr = False):
        with open(self.input_file) as rf:
            i = 0
            self._arr = []
            for line in rf:
                self._arr.append(int(line.strip()))
                if test_corr:
                    i += 1
                    print("array, ", self._arr)
                    if i > 10:
                        break


class MergeSort(SortArray):
    def __init__(self, array, input_file=None, from_file=False):
        super(MergeSort, self).__init__(array, input_file=input_file)
        self._res = []
        self.split_inverses = 0
        if from_file:
            self._arr = []
            self.read_array_file()
            self._res = self.split_sort(self.arr)
        else:
            self._res = self.split_sort(self.arr)

    @property
    def res(self):
        return self._res

    def split_sort(self, array):
        if len(array) < 2:
            return array
        middle = len(array) // 2
        result = []
        x = self.split_sort(array[:middle])
        y = self.split_sort(array[middle:])
        i, j = 0, 0
        while i < len(x) and j < len(y):
            if x[i] < y[j]:
                result.append(x[i])
                i += 1
            else:
                result.append(y[j])
                self.split_inverses += (len(x) - i)
                j += 1
        result += x[i:]
        result += y[j:]
        return result

    def naive_inverse_counting(self):
        count = 0
        print(self.arr)
        for i in range(len(self.arr)-1):
            for j in range(i+1, len(self.arr)):
                if self.arr[i] > self.arr[j]:
                    count += 1
        return count


class QuickSort(SortArray):
    def __init__(self, array=None, from_file=True, input_file=None):
        self._comparisons = 0
        if from_file:
            super(QuickSort, self).__init__([0], input_file=input_file)
            self.read_array_file()
            self.result = self.quick_sort(self.arr)
        elif array is not None:
            super(QuickSort, self).__init__(array)
            self._arr = array
            self.result = self.quick_sort(self.arr)

    def quick_sort(self, array):
        # base case
        if len(array) < 1:
            return array

        p = self.select_pivot(array, 'median')
        # print(array, array[p])
        i = 1
        # Partition Sub-Routine
        if p != 0:
            array[0], array[p] = array[p], array[0]
        p = 0
        for j in range(1, len(array)):
            if array[j] < array[p]:
                array[i], array[j] = array[j], array[i]
                i += 1
        array[p], array[i-1] = array[i-1], array[p]
        p = i-1
        # recursive calls
        x = self.quick_sort(array[:p])
        y = self.quick_sort(array[p+1:])
        # count comparisons
        if len(array) > 0:
            self._comparisons += len(array) - 1

        return x+[array[p]]+y

    def select_pivot(self, array, pivot_sel='first'):
        if pivot_sel == 'first':
            return 0
        elif pivot_sel == 'last':
            return len(array) - 1
        elif pivot_sel == 'median':
            m_arr = (len(array)-1) // 2
            strt, med, end = array[0], array[m_arr], array[-1]
            tarr = [strt, med, end]
            srt = sorted(tarr)
            if srt[1] == strt:
                return 0
            elif srt[1] == med:
                return m_arr
            else:
                return len(array) - 1

    @property
    def comparisons(self):
        return self._comparisons

if __name__ == "__main__":
    # a = list(np.random.random_integers(0, 10, 10))
    a = [10, 6, 3, 7, 9, 2, 5, 8, 1, 4]
    sorting = SortArray(a)
    print(sorting.arr)
    # Bubble sort, O(N^2), Omega(N) (don't use it)
    start_time = timeit.default_timer()
    sorting.bubble_sort()
    bub_sort_time = timeit.default_timer() - start_time
    print("Bubble sort sorted: {}".format(sorting.arr))
    # Selection sort, O(N^2), will be fastest for less than 1000 items. less overhead.
    sorting = SortArray(a)
    start_time = timeit.default_timer()
    sorting.sel_sort()
    sel_sort_time = timeit.default_timer() - start_time
    print("Selection sort sorted: {}".format(sorting.arr))
    # TODO: Insertion
    start_time = timeit.default_timer()
    from_file = True
    # input_file = './data/IntegerArray.txt'
    input_file = './data/QuickSort.txt'
    # answer: 2407905288
    sorting = MergeSort(a, input_file, from_file=from_file)
    # print(split_sort(a))
    merge_sort_time = timeit.default_timer() - start_time
    if not from_file:
        print("Merge sort sorted: {}".format(sorting.res))
    print("number of inversions: ", sorting.split_inverses)
    # print("naively calculated number of inversions: ", sorting.naive_inverse_counting())
    # Timing
    a = [10, 6, 3, 7, 9, 2, 5, 8, 1, 4]
    # 28 22 22
    # a = [8, 2, 4,5,7 ,1]
    input_file = './data/QuickSort.txt'
    start_time = timeit.default_timer()
    sorting = QuickSort(a, input_file=input_file, from_file=True)
    # 'first' - 162085 comparisons, 'last' - 164123 comparisons, 'median' - 138382
    quick_sort_time = timeit.default_timer() - start_time
    # print("QuickSort sorted array", sorting.result)
    print("The total number of comparisons is: ", sorting.comparisons)
    print("__________________________Timing__________________________________")
    print("Bubble sort: {} \nSelection sort: {} \nMerge Sort {} \nQuickSort {}".format(bub_sort_time,
                                                                     sel_sort_time,
                                                                     merge_sort_time,
                                                                     quick_sort_time))
