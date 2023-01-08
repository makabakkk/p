from line_profiler import LineProfiler
from graphviz import Digraph

class Node:
	def __init__(self, val=None,next=None):
		self.val = val
		self.next = next

class priorityQueues:
	def __init__(self):
		self.head = None
		self.length = 0

	def printList(self):
		p = self.head
		while p != None:
			print(p.val,end=" ")
			p = p.next
		print()

	def getNode(self,n):
		if n < 0 :
			return None
		p = self.head
		for i in range(0,n):
			p = p.next
		return p

	def getParent(self,idx):
		return self.getNode((idx-1)//2)

	def getLeftChild(self,idx):
		return self.getNode(2*idx+1)

	def getRightChild(self,idx):
		return self.getNode(2*idx+2)

	def pushBack(self,node):
		if self.head == None:
			self.head = node
			return;

		p = self.head
		while p.next != None:
			p = p.next
		p.next = node

	def swim(self,idx):
		t = self.getNode(idx)
		par = self.getParent(idx)

		tmpValue = t.val
		while idx > 0 and tmpValue < par.val:
			t.val = par.val # 上浮

			idx = (idx-1)//2
			t = par
			par = self.getParent(idx)
		t.val = tmpValue
	''' 
	第2小题解释：最小优先级队列实际为小根堆，插入元素时，首先采用尾插法将元素插入到链表尾部，同时将小根堆中的元素
	个数加一，最后调整最后一个元素在小根堆中的位置，调整时确定当前元素节点值和父节点值，若当前元素值小于
	父节点值，则当前元素值上浮，父节点值下沉，同时，当前指针上浮，进行下一次当前节点与父节点的比较，直到
	当前元素值大于或等于其父节点值，调整结束。

	第3小题时间复杂度分析：pushBack将元素插入链表尾部，时间复杂度为O(n),swim()函数将插入元素进行堆调整，
	随机访问条件下时间复杂度为O(logn),但由于查找左右孩子节点需要耗费O(n)时间，故时间复杂度为O(nlogn),
	故插入元素insert()时间复杂度为O(nlogn)
	'''
	# @profile
	def insert(self,val):
		self.pushBack(Node(val))
		self.length += 1
		self.swim(self.length-1)

	def sink(self,idx):
		t = self.getNode(idx)
		tmpValue = t.val
		while 2*idx+1 < self.length:
			node = self.getLeftChild(idx)
			right = self.getRightChild(idx)
			idx = idx*2 + 1
			# node指向左右孩子值较小的一个
			if right != None and right.val < node.val :
				node = right
				idx = idx*2 + 2
			if tmpValue > node.val:
				t.val = node.val
				t = node
			else:
				break
		t.val = tmpValue

	''' 
	第2小题解释：最小优先级队列实际为小根堆，删除元素时，若此时堆中元素个数大于等于2，则找到倒数第二个节点，
	将倒数第一个元素值覆盖链表头结点值，同时删除最后一个节点并将堆中元素个数减一，最后调整下标为0的
	元素在小根堆中的位置，调整时确定当前元素节点值和其左右孩子节点值，保证node指针	指向左右孩子较小
	的一个，若当前元素值大于node节点值，则当前元素值下沉，node节点值上浮，同时，当前指针
	下沉，进行下一次当前节点与左右孩子节点的比较，直到当前元素值小于或等于其左右孩子节点值，调整结束。

	第3小题时间复杂度分析：删除尾部元素时间复杂度为O(n),sink()函数将放到链表头的元素进行堆调整，
	随机访问条件下时间复杂度为O(logn),但由于查找父节点需要耗费O(n)时间，故时间复杂度为O(nlogn),
	故插入元素delMin()时间复杂度为O(nlogn)
	'''
	# @profile
	def delMin(self):
		top = self.head.val

		if self.length >= 2:
			lastTwo = self.getNode(self.length-2) # 倒数第二个元素
			self.head.val =  lastTwo.next.val # 末尾元素值放到第一个
			lastTwo.next = None # 删掉最后一个节点
			self.length -= 1 # 长度减一
			self.sink(0) # 第一个元素下沉
		else:
			self.head = None
		
		return top

	def makeTree(self):
		g = Digraph('PriorityQueues', filename='PriorityQueues.gv',format='png')

		for idx in range(0,self.length//2):
			root = self.getNode(idx)
			left = self.getLeftChild(idx)
			right = self.getRightChild(idx)

			if left != None:
				g.edge(str(root.val),str(left.val))
			if right != None:
				g.edge(str(root.val),str(right.val))

		g.view()

def insert():
	for item in [47,79,56,38,40,80,95,24]:
		pq.insert(item)

def delete():
	for i in range(0,8):
		pq.delMin()


pq = priorityQueues()
insert()
pq.makeTree()