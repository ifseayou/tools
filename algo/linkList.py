#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/20 16:07:06
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   反转链表
'''

class Node:
    def __init__(self,val=0,next=None):
        self.val = val
        self.next = next

def printLinkList(head):
    cur = head
    while cur:
        if cur.next:
            print(cur.val, end=' -> ')
        else:
            print(cur.val)
        cur = cur.next
        
def reverseLinkList(head):
    pre = None
    cur = head
    while cur:
        cur = head.next
        head.next = pre
        pre = head
        head = cur    
    return pre

if __name__ == '__main__':
    head = Node(1,Node(2,Node(3,Node(4,Node(5)))))

    printLinkList(head)

    # 反转链表
    head = reverseLinkList(head)

    printLinkList(head)

