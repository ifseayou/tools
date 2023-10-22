#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Time    :   2023/10/20 16:07:06
@Author  :   benchen
@Contact :   benchen@yowant.com
@Desc    :   反转链表 &  寻找带环链表的入环节点
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
# 反转链表        
def reverseLinkList(head):
    pre = None
    cur = head
    while cur:
        cur = head.next
        head.next = pre
        pre = head
        head = cur    
    return pre

# 返回带环节点的入环节点
def getCycleNode(head):
    if head == None or head.next == None:
        return None

    slow = head
    fast = head
    while fast != None and fast.next != None:
        slow = slow.next
        fast = fast.next.next
        if fast == slow:
            p = head
            while p != slow:
                p = p.next
                slow = slow.next
            return p
    return None
    

if __name__ == '__main__':
    n1 = Node(1)
    n2 = Node(2,n1)
    n3 = Node(3,n2)
    n4 = Node(4,n3)
    head = Node(5,n4)

    # printLinkList(n5)
    n1.next = n2
    p1 = getCycleNode(head)
    if p1 != None:
        print(p1.val)