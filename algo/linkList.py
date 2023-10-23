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

# 打印一个链表
def printLinkList(head):
    cur = head
    while cur:
        if cur.next:
            print(cur.val, end=' -> ')
        else:
            print(cur.val)
        cur = cur.next
    print() 
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


# 合并两个有序链表
def mergeTwoLists(head1, head2):
    if head1 == None :
        return head2    
    if head2 == None :
        return head1
    p1 = head1
    p2 = head2
    p = Node(99)
    head = p
    while p1 != None and p2 != None:
        if p1.val < p2.val:
            p.next = Node(p1.val)
            p = p.next
            p1 = p1.next
        else:
            p.next = Node(p2.val)
            p = p.next
            p2 = p2.next
    if p1 != None:
        p.next = p1

    if p2 != None:
        p.next = p2
    
    return head.next




if __name__ == '__main__':

    head1 = Node(-1 , Node(0, Node(3)))
    head2 = Node(4 , Node(6, Node(9)))

    printLinkList(head1)
    printLinkList(head2)
    head = mergeTwoLists(head1,head2)
    printLinkList(head)
    
