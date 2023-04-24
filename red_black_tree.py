from bloom_filter import BloomFilter

""" In-memory component of the RBT
"""
class RedBlackTree:
  def __init__(self, bloomFilterSize=1000):
    self.root = None
    self.bloom_filter = BloomFilter(bloomFilterSize) 

  def insert(self, newNode):
    # if self.root is None:
    #   self.root = newNode
    
    # curr_node = self.root

    # while curr_node.left is not None or curr_node.right is not None:
    #   if newNode.key > curr_node.key:
    #     curr_node = curr_node.left
    #   else:
    #     curr_node = curr_node.right

    # I'm growing stupid

    pass 
  
  # Might not implement delete because bloom filters might not support delete
  def delete(self, key):
    pass 

  def retrieve(self, key):
    pass

class Node:
  """ Node class for a tree. 
  According to the LSM Architecture, we will assume that the key is of int with value of a fixed length string.
  """
  def __init__(self, color, key, value="node content created"):
    self.color = color
    self.key = key
    self.value = value 
    self.right = None 
    self.left = None 

  def setRight(self, rightNode):
    self.right = rightNode 
  
  def setLeft(self, leftNode):
    self.left = leftNode
  
