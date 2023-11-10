#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/26 19:11:08
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

#判断  '[]{()}()' 是否是正常的表达式
import re


def isParentheses(s):
    stack = []
    for i in s:
        if i == '{' or i == '[' or i == '(':
            stack.append(i)

        if i == '}':
            if len(stack) ==0 or '{' != stack.pop():
                return False
        if i == ']':
            if len(stack) ==0 or '[' != stack.pop():
                return False
        if i == ')':
            if len(stack) ==0 or '(' != stack.pop():
                return False
    return len(stack) ==0


# 最小栈
class MinStack(object):
    def __init__(self):
        self.dataStack = []
        self.minStack = []

    def push(self,num): # 入栈
        self.dataStack.append(num)
        if not self.minStack :
            self.minStack.append(num)
        else:
            if self.minStack[-1] > num:
                self.minStack.append(num)
            else:
                self.minStack.append(self.minStack[-1])

    def pop(self): # 出栈
        if self.dataStack:
            self.minStack.pop()
            return self.dataStack.pop() 

    def top(self): # 查看栈顶元素
        if self.dataStack:
            self.dataStack[-1]
        

    def getMin(self): # 查看栈内最小元素
        if self.minStack:
            return self.minStack[-1]




# backspace问题

def backspaceCompare(s1,s2):
    def backspace(s):
        stack = []
        for c in s:
            if c != '#':
                stack.append(c)
            elif stack: # stack is not empty
                stack.pop()
        print(stack)
        return stack    
        
    return backspace(s1) == backspace(s2)
 


# 篮球计分问题
def calPoints(operations):
    stack1 =  []
    for op in operations:
        if op == "C" :
            stack1.pop()
        elif op == "D":
            stack1.append(stack1[-1] * 2)
        elif op == "+":
            a = stack1.pop()
            b = stack1.pop()
            stack1.append(b)
            stack1.append(a)
            stack1.append(a + b)
        else:
            stack1.append(int(op))
    sum = 0
    for i in stack1:
        sum = sum + i
    return sum

# leetcode 496 下一个更大的元素 ， O(n)
def nextGreaterElement(nums1, nums2):
    res = []
    stack = []
    help = {}

    for num in nums2:
        while(stack and stack[-1] < num):
            help[stack.pop()] = num
        stack.append(num)
    
    for num in nums1:
        res.append(help.get(num,-1))

    return res


if __name__ == '__main__':
    nums1 = [4, 1, 2]
    nums2 = [1, 0, -1, -2, 3, 4, 2, 99]
    res = nextGreaterElement(nums1,nums2)
    print(res)
