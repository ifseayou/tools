5 -> 4 -> 3 -> 2 -> 1 - > 3

第一次：
s = 5
f = 5 
  

第二次
s = 4 
f = 3


第三次
s = 3
f = 1

第四次
s = 2
f = 2

新的循环：

第五次
s = 1
f = 1  -- 入环节点 = f.next

第六次
s = 4
f = 3




对于一个单链表， 判断这个链表是否为带环链表，如果是 返回入环节点，Java 实现

比如输入为： 5 -> 4 -> 3 -> 2 -> 1 -> 3 
返回为：3