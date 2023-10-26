#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/26 19:11:08
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   None
'''

#判断  '[]{()}()' 是否是正常的表达式
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

if __name__ == '__main__':
    res = isParentheses('[]{()}()')
    print(0.3 + 0.6) # 0.8999999999999999
