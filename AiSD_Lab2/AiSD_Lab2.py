import random
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import math

class BinaryTree:
    def __init__(self, key):
        self.key = key
        self.l = None
        self.r = None
        self.height = 1

    def height(key):
        if not key:
            return 0
        return key.height

    def insert(self, new_key):
        if self is None:
            self = BinaryTree(new_key)  
            return self
        if new_key < self.key:
            self.l = BinaryTree.insert(self.l, new_key)
        else:
            self.r = BinaryTree.insert(self.r, new_key)
        self.height = 1 + max(BinaryTree.height(self.l), BinaryTree.height(self.r))
        return self

    def search(self, find_key):
      if self.key == find_key:    
        #print("Найденное значение = ", self.key)
        return
      if find_key < self.key:   
            if self.l:   
                BinaryTree.search(self.l,find_key)
            #else:
                #print("Значение не найдено")
      else:
            if self.r:
                BinaryTree.search(self.r,find_key)
            #else:   
                #print("Значение не найдено") 

    def delete(self, delete_key):
        if self is None:
            return self
        if delete_key < self.key:
            self.l = BinaryTree.delete(self.l, delete_key)
        elif(delete_key > self.key):
            self.r = BinaryTree.delete(self.r, delete_key)
        else:
            if self.l is None:
                temp = self.r
                self = None
                #print("Удалено значение = ", delete_key)
                return temp
            elif self.r is None:
                temp = self.l
                self = None
                #print("Удалено значение = ", delete_key)
                return temp
            current = self.r
            while(current.l is not None):
                current = current.l
            temp = current
            self.key = temp.key
            self.r = BinaryTree.delete(self.r, temp.key)
            self.height = 1 + max(BinaryTree.height(self.l), BinaryTree.height(self.r))
        return self

class RBConstruct:
    def __init__(self, key, color='red'):
        self.key = key
        self.color = color
        self.l = None
        self.r = None
        self.parent = None

    def grandparent(self):
        if self.parent is None:
            return None
        return self.parent.parent

    def sibling(self):
        if self.parent is None:
            return None
        if self == self.parent.l:
            return self.parent.r
        return self.parent.l

    def uncle(self):
        if self.parent is None:
            return None
        return self.parent.sibling()


class RedBlackTree:
    def __init__(self):
        self.root = None

    def height(self, key):
        if key is None:
            return 0
        else:
            height_l = 1 + self.height(key.l)
            height_r = 1 + self.height(key.r)
            return max(height_l, height_r)

    def final_height(self):
        if self.root is None:
            return 0
        height = (self.height(self.root)) - 1
        return height

    def insert(self, key):
            new_key = RBConstruct(key)
            if self.root is None:
                self.root = new_key
            else:
                curr = self.root
                while True:
                    if key < curr.key:
                        if curr.l is None:
                            curr.l = new_key
                            new_key.parent = curr
                            break
                        else:
                            curr = curr.l
                    else:
                        if curr.r is None:
                            curr.r = new_key
                            new_key.parent = curr
                            break
                        else:
                            curr = curr.r
            self.insert_balanced(new_key) 

    def search(self, key):
        curr = self.root
        while curr is not None:
            if key == curr.key:
                #print("Найденное значение = ", curr.key)
                return curr
            elif key < curr.key:
                curr = curr.l
            else:
                curr = curr.r
        #print("Значение не найдено")
        return None


    def delete(self, key):
        delete_key = self.search(key)
        if delete_key is None:
            #print("Значение не найдено")
            return
        color = delete_key.color
        if delete_key.l is None or delete_key.r is None:
            if delete_key.parent is None:
                self.root = delete_key.l or delete_key.r
            else:
                if delete_key == delete_key.parent.l:
                    delete_key.parent.l = delete_key.l or delete_key.r
                else:
                    delete_key.parent.r = delete_key.l or delete_key.r
            if delete_key.l is not None or delete_key.r is not None:
                (delete_key.l or delete_key.r).parent = delete_key.parent
            #print("Удалено значение = ", key)
        else:
            successor = delete_key.r
            while successor.l is not None:
                successor = successor.l
            delete_key.key = successor.key
            if successor.parent is None:
                self.root = successor.r
            else:
                if successor == successor.parent.l:
                    successor.parent.l = successor.r
                else:
                    successor.parent.r = successor.r
            if successor.r is not None:
                successor.r.parent = successor.parent
            print("Удалено значение = ", key)
        self.delete_balanced(delete_key)


    def insert_balanced(self, x):
        while x.parent and x.parent.color == 'red':
            if x.parent == x.grandparent().l:
                uncle = x.uncle()
                if uncle and uncle.color == 'red':
                    x.parent.color = 'black'
                    uncle.color = 'black'
                    x.grandparent().color = 'red'
                    x = x.grandparent()
                else:
                    if x == x.parent.r:
                        x = x.parent
                        self.rotate_l(x)
                    x.parent.color = 'black'
                    x.grandparent().color = 'red'
                    self.rotate_r(x.grandparent())
            else:
                uncle = x.uncle()
                if uncle and uncle.color == 'red':
                    x.parent.color = 'black'
                    uncle.color = 'black'
                    x.grandparent().color = 'red'
                    x = x.grandparent()
                else:
                    if x == x.parent.l:
                        x = x.parent
                        self.rotate_r(x)
                    x.parent.color = 'black'
                    x.grandparent().color = 'red'
                    self.rotate_l(x.grandparent())
        self.root.color = 'black'

    def delete_balanced(self, x):
        while x != self.root and x.color == 'black':
            if x == x.parent.l:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_l(x.parent)
                    sibling = x.sibling()
                if (sibling.l is None or sibling.l.color == 'black') and (sibling.r is None or sibling.r.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.r is None or sibling.r.color == 'black':
                        sibling.l.color = 'black'
                        sibling.color = 'red'
                        self.rotate_r(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.r:
                        sibling.r.color = 'black'
                    self.rotate_l(x.parent)
                    x = self.root
            else:
                sibling = x.sibling()
                if sibling.color == 'red':
                    sibling.color = 'black'
                    x.parent.color = 'red'
                    self.rotate_r(x.parent)
                    sibling = x.sibling()
                if (sibling.l is None or sibling.l.color == 'black') and (sibling.r is None or sibling.r.color == 'black'):
                    sibling.color = 'red'
                    x = x.parent
                else:
                    if sibling.l is None or sibling.l.color == 'black':
                        sibling.r.color = 'black'
                        sibling.color = 'red'
                        self.rotate_l(sibling)
                        sibling = x.sibling()
                    sibling.color = x.parent.color
                    x.parent.color = 'black'
                    if sibling.l:
                        sibling.l.color = 'black'
                    self.rotate_r(x.parent)
                    x = self.root
        x.color = 'black'

    def rotate_l(self, root):
        son1 = root.r
        root.r = son1.l
        if son1.l is not None:
            son1.l.parent = root
        son1.parent = root.parent
        if root.parent is None:
            self.root = son1
        elif root == root.parent.l:
            root.parent.l = son1
        else:
            root.parent.r = son1
        son1.l = root
        root.parent = son1

    def rotate_r(self, root):
        son2 = root.l
        root.l = son2.r
        if son2.r is not None:
            son2.r.parent = root
        son2.parent = root.parent
        if root.parent is None:
            self.root = son2
        elif root == root.parent.r:
            root.parent.r = son2
        else:
            root.parent.l = son2
        son2.r = root
        root.parent = son2

class AVLConstruct:
    def __init__(self, key):
        self.key = key
        self.l = None
        self.r = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if not node:
            return 0
        return node.height

    def balance(self, node):
        if not node:
            return 0
        return self.height(node.l) - self.height(node.r)

    def insert(self, root, key):
        if not root:
            return AVLConstruct(key)
        elif key < root.key:
            root.l = self.insert(root.l, key)
        else:
            root.r = self.insert(root.r, key)
        root.height = 1 + max(self.height(root.l), self.height(root.r))
        balance = self.balance(root)
        if balance > 1 and key < root.l.key:
            return self.r_rotate(root)
        if balance < -1 and key > root.r.key:
            return self.l_rotate(root)
        if balance > 1 and key > root.l.key:
            root.l = self.l_rotate(root.l)
            return self.r_rotate(root)
        if balance < -1 and key < root.r.key:
            root.r = self.r_rotate(root.r)
            return self.l_rotate(root)
        return root

    def delete(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.l = self.delete(root.l, key)
        elif key > root.key:
            root.r = self.delete(root.r, key)
        else:
            if not root.l:
                temp = root.r
                root = None
                return temp
            elif not root.r:
                temp = root.l
                root = None
                return temp
            current = root.r
            while(current is not None and current.l is not None):
                current = current.l
            root.key = current.key
            root.r = self.delete(root.r, current.key)
        root.height = 1 + max(self.height(root.l), self.height(root.r))
        if not root:
            return root
        root.height = 1 + max(self.height(root.l), self.height(root.r))
        balance = self.balance(root)
        if balance > 1 and self.balance(root.l) >= 0:
            return self.r_rotate(root)
        if balance < -1 and self.balance(root.r) <= 0:
            return self.l_rotate(root)
        if balance > 1 and self.balance(root.l) < 0:
            root.l = self.l_rotate(root.l)
            return self.r_rotate(root)
        if balance < -1 and self.balance(root.r) > 0:
            root.r = self.r_rotate(root.r)
            return self.l_rotate(root)
        return root

    def l_rotate(self, root):
        son1 = root.r
        grandson = son1.l
        son1.l = root
        root.r = grandson
        root.height = 1 + max(self.height(root.l), self.height(root.r))
        son1.height = 1 + max(self.height(son1.l), self.height(son1.r))
        return son1

    def r_rotate(self, root):
        son1 = root.l
        grandson = son1.r
        son1.r = root
        root.l = grandson
        root.height = 1 + max(self.height(root.l), self.height(root.r))
        son1.height = 1 + max(self.height(son1.l), self.height(son1.r))
        return son1

    def search(self, root, key):
        if not root or root.key == key:
            #print("Найденно значение ", key)
            return root
        if root.key < key:
            return self.search(root.r, key)
        return self.search(root.l, key)

    def insert_key(self, key):
        self.root = self.insert(self.root, key)

    def delete_key(self, key):
        self.root = self.delete(self.root, key)
        #print("Удалено значение ", key) 

    def search_key(self, key):
        return self.search(self.root, key)

def dfs_1(self, root):
    if root:
        dfs_1(self, root.l)
        print(root.key, end=' ')
        dfs_1(self, root.r)
def dfs_2(self, root):
    if root:
        print(root.key, end=' ')
        dfs_2(self, root.l)
        dfs_2(self, root.r)
def dfs_3(self, root):
    if root:
        dfs_3(self, root.l)
        dfs_3(self, root.r)
        print(root.key, end=' ')
        
def bfs(root):
    if root:
        queue = [root]
        while queue:
            node = queue.pop(0)
            print(node.key, end=' ')
            if node.l:
                queue.append(node.l)
            if node.r:
                queue.append(node.r)


random.seed(1)
key_count = 100
max_key = 1000
height_arr=[]
key_count_arr = []

binary_key = [randint(1,max_key) for i in range(key_count)]
binary_tree = BinaryTree(binary_key[0])
for i in range(1,key_count):
    binary_tree.insert(binary_key[i])
binary_tree.search(binary_key[randint(0,key_count-1)])
binary_tree.delete(binary_key[randint(0,key_count-1)])
print("Двоичное дерево поиска, обходы в глубину: ")
dfs_1(binary_tree, binary_tree)
print()
dfs_2(binary_tree, binary_tree)
print()
dfs_3(binary_tree, binary_tree)
print("\nв ширину: ")
bfs(binary_tree)
print("\nКорень ", binary_tree.key, " высота ", binary_tree.height)
print()

RB_key = [randint(1,max_key) for i in range(key_count)]
RB_tree = RedBlackTree()
for i in range(key_count):
    RB_tree.insert(RB_key[i])
RB_tree.search(RB_key[randint(0,key_count-1)])
RB_tree.delete(RB_key[randint(0,key_count-1)])
print("RB дерево, обходы в глубину: ")
dfs_1(RB_tree, RB_tree.root)
print()
dfs_2(RB_tree, RB_tree.root)
print()
dfs_3(RB_tree, RB_tree.root)
print("\nв ширину: ")
bfs(RB_tree.root)
print("\nКорень ", RB_tree.root.key , " высота ", RB_tree.final_height())
print()

AVL_key=[randint(1,max_key) for i in range(key_count)]
AVL_tree = AVLTree()
for i in range(key_count):
    AVL_tree.insert_key(AVL_key[i])
AVL_tree.search_key(AVL_key[randint(0,key_count-1)])
AVL_tree.delete_key(AVL_key[randint(0,key_count-1)])
print("AVL дерево, обходы в глубину: ")
dfs_1(AVL_tree, AVL_tree.root)
print()
dfs_2(AVL_tree, AVL_tree.root)
print()
dfs_3(AVL_tree, AVL_tree.root)
print("\nв ширину: ")
bfs(AVL_tree.root)
print("\nКорень ", AVL_tree.root.key , " высота ", AVL_tree.root.height)
#theory_up=[]
#theory_down=[]
#for j in range(10):
#    AVL_key=[i for i in range(key_count)]
#    AVL_tree=AVLTree()
#    for i in range(key_count):
#        AVL_tree.insert_key(AVL_key[i])
#    key_count_arr.append(key_count)
#    height_arr.append( AVL_tree.root.height)
#    theory_up.append((math.log(key_count,1.63)+1))
#    theory_down.append(math.log(key_count,2))
#    key_count+=1000

#print(key_count_arr)
#print(height_arr)
#plt.plot(key_count_arr,height_arr,label = "practical result", marker='o',markersize = 4,color="b")
#plt.plot(key_count_arr,theory_up,label = "upper estimates", marker='o',markersize = 4,color="r")
#plt.plot(key_count_arr,theory_down,label = "asymptotics", marker='o',markersize = 4,color="g")
#sizes = np.array(key_count_arr)
#heights = np.array(height_arr)
#coeffs = np.polyfit(sizes, heights, 2)
#poly = np.poly1d(coeffs)
#print(poly)
#plt.scatter(sizes, heights, color='blue')
#plt.plot(sizes, poly(sizes), color='red')
#plt.xlabel('Number of keys')
#plt.ylabel('Height of the tree')
#plt.title ('AVL tree')
#plt.legend()
#plt.savefig("221.png")
#plt.show()


