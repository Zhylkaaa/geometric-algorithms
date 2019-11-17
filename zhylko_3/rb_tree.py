import string

# all credit to: https://github.com/MSingh3012/Red-Black-tree-in-python/blob/master/RBTree.py?fbclid=IwAR3LjX2Zr6-XzXAkUaVt8-0T6hx07FRVrAe2soL8ESvTXoohzJX9bPBpDCc

# small bug fixes and additions: github.com/Zhylkaaa

BLACK = 0
RED = 1

class RBNode(object):

    def __init__(self, key = None, value = None, color = RED):
        self.left = self.right = self.parent = None
        self.color = color
        self.key = key
        self.value = value
        self.nonzero = 1

    def __str__(self):
        return repr(self.key) + ': ' + repr(self.value)

    def __nonzero__(self):
        return self.nonzero

    def __len__(self):
        """imitate sequence"""
        return 2

    def __getitem__(self, index):
        """imitate sequence"""
        if index==0:
            return self.key
        if index==1:
            return self.value
        raise IndexError('only key and value as sequence')


class RBTreeIter(object):

    def __init__ (self, tree):
        self.tree = tree
        self.index = -1  # ready to iterate on the next() call
        self.node = None
        self.stopped = False

    def __iter__ (self):
        """ Return the current item in the container
        """
        return self.node.value

    def next (self):
        """ Return the next item in the container
            Once we go off the list we stay off even if the list changes
        """
        if self.stopped or (self.index + 1 >= self.tree.__len__()):
            self.stopped = True
            raise StopIteration
        #
        self.index += 1
        if self.index == 0:
            self.node = self.tree.firstNode()
        else:
            self.node = self.tree.nextNode (self.node)
        return self.node.value


class RBTree(object):

    def __init__(self,):
        self.sentinel = RBNode()
        self.sentinel.left = self.sentinel.right = self.sentinel
        self.sentinel.color = BLACK
        self.sentinel.nonzero = 0
        self.root = self.sentinel
        self.count = 0

    def __len__(self):
        return self.count

    def __del__(self):
        # unlink the whole tree

        s = [ self.root ]

        if self.root is not self.sentinel:
            while s:
                cur = s[0]
                if cur.left and cur.left != self.sentinel:
                    s.append(cur.left)
                if cur.right and cur.right != self.sentinel:
                    s.append(cur.right)
                cur.right = cur.left = cur.parent = None
                cur.key = cur.value = None
                s = s[1:]

        self.root = None
        self.sentinel = None

    def __str__(self):
        return "<RBTree object>"

    def __repr__(self):
        return "<RBTree object>"

    def __iter__ (self):
        return RBTreeIter (self)

    def rotateLeft(self, x):

        y = x.right

        # establish x.right link
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        else:
            self.root = y

        # link x and y
        y.left = x
        if x != self.sentinel:
            x.parent = y

    def rotateRight(self, x):

        #***************************
        #  rotate node x to right
        #***************************

        y = x.left

        # establish x.left link
        x.left = y.right
        if y.right != self.sentinel:
            y.right.parent = x

        # establish y.parent link
        if y != self.sentinel:
            y.parent = x.parent
        if x.parent:
            if x == x.parent.right:
                x.parent.right = y
            else:
                x.parent.left = y
        else:
            self.root = y

        # link x and y
        y.right = x
        if x != self.sentinel:
            x.parent = y

    def insertFixup(self, x):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after inserting node x           *
        #************************************

        # check Red-Black properties

        while x != self.root and x.parent.color == RED:

            # we have a violation

            if x.parent == x.parent.parent.left:

                y = x.parent.parent.right

                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent

                else:
                    # uncle is BLACK
                    if x == x.parent.right:
                        # make x a left child
                        x = x.parent
                        self.rotateLeft(x)

                    # recolor and rotate
                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    self.rotateRight(x.parent.parent)
            else:

                # mirror image of above code

                y = x.parent.parent.left

                if y.color == RED:
                    # uncle is RED
                    x.parent.color = BLACK
                    y.color = BLACK
                    x.parent.parent.color = RED
                    x = x.parent.parent

                else:
                    # uncle is BLACK
                    if x == x.parent.left:
                        x = x.parent
                        self.rotateRight(x)

                    x.parent.color = BLACK
                    x.parent.parent.color = RED
                    self.rotateLeft(x.parent.parent)

        self.root.color = BLACK

    def insert(self, key):
        #**********************************************
        #  allocate node for data and insert in tree  *
        #**********************************************

        # find where node belongs
        current = self.root
        parent = None
        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            # rc = self.__cmp(key, current.key)
            if key == current.key:
                return current
            parent = current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        # setup new node
        x = RBNode(key, None)
        x.left = x.right = self.sentinel
        x.parent = parent

        self.count = self.count + 1

        # insert node in tree
        if parent:
            if key < parent.key:
                parent.left = x
            else:
                parent.right = x
        else:
            self.root = x

        self.insertFixup(x)
        return x

    def deleteFixup(self, x):
        #************************************
        #  maintain Red-Black tree balance  *
        #  after deleting node x            *
        #************************************

        while x != self.root and x.color == BLACK:
            if x == x.parent.left:
                w = x.parent.right
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotateLeft(x.parent)
                    w = x.parent.right

                if w.left.color == BLACK and w.right.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.right.color == BLACK:
                        w.left.color = BLACK
                        w.color = RED
                        self.rotateRight(w)
                        w = x.parent.right

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.right.color = BLACK
                    self.rotateLeft(x.parent)
                    x = self.root

            else:
                w = x.parent.left
                if w.color == RED:
                    w.color = BLACK
                    x.parent.color = RED
                    self.rotateRight(x.parent)
                    w = x.parent.left

                if w.right.color == BLACK and w.left.color == BLACK:
                    w.color = RED
                    x = x.parent
                else:
                    if w.left.color == BLACK:
                        w.right.color = BLACK
                        w.color = RED
                        self.rotateLeft(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = BLACK
                    w.left.color = BLACK
                    self.rotateRight(x.parent)
                    x = self.root

        x.color = BLACK

    def deleteNode(self, z):
        #****************************
        #  delete node z from tree  *
        #****************************

        if not z or z == self.sentinel:
            return

        if z.left == self.sentinel or z.right == self.sentinel:
            # y has a self.sentinel node as a child
            y = z
        else:
            # find tree successor with a self.sentinel node as a child
            y = z.right
            while y.left != self.sentinel:
                y = y.left

        # x is y's only child
        if y.left != self.sentinel:
            x = y.left
        else:
            x = y.right

        # remove y from the parent chain
        x.parent = y.parent
        if y.parent:
            if y == y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        else:
            self.root = x

        if y != z:
            z.key = y.key
            z.value = y.value

        if y.color == BLACK:
            self.deleteFixup(x)

        del y
        self.count = self.count - 1

    def findNode(self, key):
        #******************************
        #  find node containing data
        #******************************

        current = self.root

        while current != self.sentinel:
            # GJB added comparison function feature
            # slightly improved by JCG: don't assume that ==
            # is the same as self.__cmp(..) == 0
            #rc = self.__cmp(key, current.key)
            
            if key == current.key:
                return current
            else:
                if key < current.key:
                    current = current.left
                else:
                    current = current.right

        return None
    
    def remove(self, key):
        node = self.findNode(key)
        self.deleteNode(node)

    def traverseTree(self, f):
        if self.root == self.sentinel:
            return
        s = [ None ]
        cur = self.root
        while s:
            if cur.left:
                s.append(cur)
                cur = cur.left
            else:
                f(cur)
                while not cur.right:
                    cur = s.pop()
                    if cur is None:
                        return
                    f(cur)
                cur = cur.right
        # should not get here.
        return

    def nodesByTraversal(self):
        """return all nodes as a list"""
        result = []
        def traversalFn(x, K=result):
            K.append(x)
        self.traverseTree(traversalFn)
        return result

    def nodes(self):
        """return all nodes as a list"""
        cur = self.firstNode()
        result = []
        while(not cur is self.sentinel and not cur is None):
            result.append(cur.key)
            cur = self.nextNode(cur)
        return result

    def minimum(self):
        cur = self.root
        
        if self.root is None:
            return None
        
        while not cur.left is self.sentinel:
            cur = cur.left
            
        return cur.key

    def maximum(self):
        cur = self.root
        
        if self.root is None:
            return None
        
        while not cur.right is self.sentinel:
            cur = cur.right
            if cur is self.sentinel:
                return None
        return cur.key
    
    def firstNode(self):
        cur = self.root
        
        if self.root is None:
            return None
        
        while not cur.left is self.sentinel:
            cur = cur.left
            
        return cur
    
    def nextNode(self, prev):
        cur = prev
        
        if cur is None:
            return None
        
        if not cur.right is self.sentinel:
            cur = prev.right
            while not cur.left is self.sentinel:
                cur = cur.left
            return cur
        while 1:
            cur = cur.parent
            if cur is None or cur is self.sentinel:
                return None
            if prev.key < cur.key or prev.key == cur.key:
                return cur
    
    def successor(self, prev):
        """returns None if there isn't one"""
        prev = self.findNode(prev)
        
        cur = prev
        
        if cur is None:
            return None
        
        if not cur.right is self.sentinel:
            cur = prev.right
            while not cur.left is self.sentinel:
                cur = cur.left
            return cur.key
        while 1:
            cur = cur.parent
            if cur is None or cur is self.sentinel:
                return None
            if prev.key < cur.key or prev.key == cur.key:
                return cur.key

    def predecessor(self, next):
        """returns None if there isn't one"""
        next = self.findNode(next)
        
        cur = next
        
        if cur is None:
            return None
        
        if not cur.left is self.sentinel:
            cur = next.left
            while not cur.right is self.sentinel:
                cur = cur.right
            return cur.key
        while 1:
            cur = cur.parent
            if cur is None or cur is self.sentinel:
                return None
            if cur.key < next.key or next.key == cur.key:
                return cur.key

