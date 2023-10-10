#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/10 16:54:54
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   排序算法
'''

def bubbleSort(arr):
    if arr == None or len(arr) <= 1:
        return
    
    n = len(arr)
    for i in range( n - 1):
        for j in range( n - i - 1):
            if arr[j] > arr[j+1]:
                arr[j],arr[j+1] = arr[j+1],arr[j]


def selectSort(arr):
    if arr == None or len(arr) <= 1:
        return

    n = len(arr)
    for i in range(n - 1):
        minIdx = i

        for j in range(i + 1, n):
            if arr[j] < arr[minIdx]:
                minIdx = j
        arr[i],arr[minIdx] = arr[minIdx],arr[i]



if __name__ == '__main__':
    arr = [1,4,8,2,3,0]

    # bubbleSort(arr)    
    # bubbleSort(arr)

    # test the select sort 
    selectSort(arr)

    for i in arr :
        print(i,end="\t")    

