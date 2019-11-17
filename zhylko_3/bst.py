class BST:
    
    class Node():
        def __init__(self, key=None):
            self.left = None
            self.right = None
            self.p = None
            self.key = key
    
    def __init__(self):
        self.root = None
    
    def insert(self, key):
        node = self.Node(key=key)
        
        x = self.root
        y = None
        
        while(not x is None):
            y = x
            if(x.key < node.key):
                x = x.right
            else:
                x = x.left
        node.p = y
        
        if(y is None):
            self.root = node
        elif(y.key < node.key):
            y.right = node
        else:
            y.left = node
            
    def find(self, key):
        x = self.root
        
        if(x is None):
            print("Tree error in method find: can't find element tree is empty")
            return
        
        while(not x is None):
            if(x.key < key):
                x = x.right
            elif(x.key == key):
                return x
            else:
                x = x.left
        print("Tree error in method find: can't find element, key=",key,"does not exist")
        return None
    
    def remove(self, key):
        node = self.find(key)
        
        if(node is None):
            print("Tree error in method remove: key",key,"does not exist")
            #raise RuntimeError('trying to remove unexisting key')
            return
        
        if(self.root is None):
            print("Tree error in method remove: can't remove element from empty tree")
            return
        
        if(not node.left is None):
            
            if(not node.right is None):
                right_most = node.left
                while(not right_most.right is None):
                    right_most = right_most.right
                right_most.right = node.right
                node.right.p = right_most
                
                
            node.left.p = node.p
            
            if node is self.root:
                self.root = node.left
            else:
                if(node.p.left is node):
                    node.p.left = node.left
                else:
                    node.p.right = node.left
            return
        
        if(not node.right is None):
            node.right.p = node.p
            
            if node is self.root:
                self.root = node.right
            else:
                if node.p.left is node:
                    node.p.left = node.right
                else:
                    node.p.right = node.right
            return
        
        if(node is self.root):
            self.root = None
        else:
            if(node is node.p.left):
                node.p.left = None
            else:
                node.p.right = None
        return
    
    def predecessor(self, key):
        node = self.find(key)
        if(node is None):
            print("Tree error in method predecessor: key",key, "does not exist!")
            return None
        
        if not node.left is None:
            node = node.left
            while(not node.right is None):
                node = node.right
            return node.key
        while( (not node.p is None) and node.p.left is node ):
              node = node.p
              
        if not node.p is None:
            return node.p.key
        else:
            return None
        
    def successor(self, key):
        node = self.find(key)
        if(node is None):
            print("Tree error in method successor: key",key, "does not exist!")
            return None
        
        if not node.right is None:
            node = node.right
            while(not node.left is None):
                node = node.left
            return node.key
        while( (not node.p is None) and node.p.right is node):
            node = node.p
        if not node.p is None:
            return node.p.key
        else:
            return None
    
    def maximum(self):
        if(self.root is None):
            print("Tree error in method maximum: can't find maximum element if empty tree")
            return None
        
        node = self.root
        while(not node.right is None):
            node = node.right
        return node.key
    
    def minimum(self):
        if(self.root is None):
            print("Tree error in method minimum: can't find minimum element if empty tree")
            return None
        
        node = self.root
        while(not node.left is None):
            node = node.left
        return node.key
    