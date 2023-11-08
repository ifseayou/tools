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
 

if __name__ == '__main__':
    a = "124###a#ab"
    b = "124###ab#b"
    print(backspaceCompare(a,b))
    

