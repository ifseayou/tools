#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/10 16:54:54
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   排序算法
'''

from random import randint


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

def insertSort(arr):
    if arr == None or len(arr) <= 1:
        return

    n = len(arr)
    for i in range(1,n):
        for j in range(i,0,-1):
            if arr[j] <  arr[j-1]:
                arr[j],arr[j-1] = arr[j-1], arr[j]


def mergeSort(arr):
    if arr == None or len(arr) <= 1:
        return

    n = len(arr)

    sortProcess(arr,0,n - 1)


def sortProcess(arr,L,R):
    if L >= R:
        return
    
    middle = int(L + (R - L) / 2)
    sortProcess(arr,L,middle)
    sortProcess(arr,middle+1,R)
    merge(arr,L,middle,R)
    

def merge(arr,L,middle,R):
    help = [0] * (R - L + 1)
    p1 = L
    p2 = middle + 1
    i = 0
    while  p1 <= middle and p2 <= R:
        if arr[p1] <= arr[p2]:
            print(p1)
            help[i] = arr[p1]
            p1 = p1 + 1
            i = i + 1
        else:
            help[i] = arr[p2]
            p2 = p2 +1
            i = i + 1 
    
    while p1 <= middle:
        help[i] = arr[p1]
        i = i + 1
        p1 = p1 + 1

    while p2 <= R:
        help[i] = arr[p2]
        i = i + 1
        p2 = p2 + 1

    for j in range(len(help)):
        arr[L+j] = help[j]


def quickSort(arr):
    if arr == None or len(arr) <= 1:
        return

    n = len(arr)

    process(arr,0,n - 1)


def process(arr,L,R):
    if L < R : 
        idx = randint(L,R-1)
        arr[R] , arr[idx] =   arr[idx] , arr[R]

        # return the equal index scope 
        p1,p2 = partition(arr,L,R)
        process(arr,L , p1 -1)
        process(arr, p2 +1 , R)

def partition(arr,L,R):
    less = L - 1 
    more = R 
    while L < more :
        if arr[L] < arr[R]:
            less = less + 1
            arr[less] , arr[L] =   arr[L] , arr[less]
            L = L + 1

        elif arr[L] > arr[R]:
            more =  more -1
            arr[more] , arr[L] =   arr[L] , arr[more]
        else:
            L = L + 1
    arr[R], arr[more] = arr[more],arr[R]
    
    return less + 1 , more





if __name__ == '__main__':
    arr = [1,4,8,0,2,3,0]

    # test the bubble sort
    # bubbleSort(arr)

    # test the select sort 
    # selectSort(arr)

    # test the insert sort
    # insertSort(arr)

    # test the merge sort
    # mergeSort(arr)

    # test the quick sort
    quickSort(arr)



    for i in arr :
        print(i,end="\t")    

