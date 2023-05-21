from BloomFilter import BloomFilter

""" In-memory component (memtable) of the LSM Architecture.
It just has to be a self balancing node.  
"""
class AVL_Tree:
  def __init__(self, bloomFilterSize=1000, maxElements=1000):
    self.root = None
    self.len_counter = 0
    self.max_elements = maxElements
    self.bloom_filter = BloomFilter(bloomFilterSize)

  def search(self, target):

    # Check bloom filter first
    if not self.bloom_filter.membership_check(target):
      raise KeyError(f"Key {target} not found in tree. Bloom Filter says so.") 

    return self._search(self.root, target)
  
  def _search(self, root, target):
    if root is None:
      raise KeyError(f"Key {target} not found in tree.") 

    if root.key == target:
      return root 

    elif root.key < target: 
      return self._search(root.right, target)

    else:
      return self._search(root.left, target)

    return None 
  
  def insert(self, newNode):

    if self.root is None:
      self.root = newNode
      return 

    try:
      self._insert(self.root, newNode)

      # If insert was successful, update bloom filter and length counter
      self.bloom_filter.insert(newNode.key)
      self.len_counter += 1
    except KeyError as e:
      print(e)
      return

  def _insert(self, root, newNode):
    if root is None:
      return newNode

    # Traverse down the tree to insert the correct node
    if newNode.key > root.key:
      root.right = self._insert(root.right, newNode) 
    
    elif newNode.key < root.key:
      root.left = self._insert(root.left, newNode)

    elif newNode.key == root.key:
      raise KeyError(f"Key {newNode.key} already exists in tree. Please call the update function instead.")

    # As coming up from the tree, we want to change height and calculate balance factor
    root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))

    # Calculate balance factor
    left_height = 0 if root.left is None else root.left.height 
    right_height = 0 if root.right is None else root.right.height 
    balance_factor = right_height - left_height 

    if balance_factor > 1 and (root.right is None or newNode.key > root.right.key):
      return self._right_rotate(root)

    if balance_factor < -1 and (root.left is None or newNode.key < root.left.key):
        return self._left_rotate(root)

    if balance_factor > 1 and (root.left is not None and newNode.key > root.left.key):
        root.left = self._left_rotate(root.left)
        return self._right_rotate(root)

    if balance_factor < -1 and (root.right is not None and newNode.key < root.right.key):
        root.right = self._right_rotate(root.right)
        return self._left_rotate(root)

    return root  

  def _right_rotate(self, head):
    # The right side becomes the head
    new_head = head.left
    if new_head is None:
        return head
    head.left = new_head.right 
    new_head.right = head

    # Update height of nodes 
    head.height = 1 + max(self._get_height(head.left), self._get_height(head.right)) 
    new_head.height = 1 + max(self._get_height(new_head.left), self._get_height(new_head.right))
    
    return new_head 

  def _left_rotate(self, head):
    new_head = head.right 
    if new_head is None:
        return head

    head.right = new_head.left 
    if head.right is not None:
        head.right.parent = head  # Update parent reference

    new_head.left = head 

    # Update the height of the node 
    head_height = head.left.height if head.left is not None else 0
    right_height = head.right.height if head.right is not None else 0
    head.height = 1 + max(head_height, right_height)

    new_head_height = new_head.left.height if new_head.left is not None else 0
    new_head_right_height = new_head.right.height if new_head.right is not None else 0
    new_head.height = 1 + max(new_head_height, new_head_right_height)

    return new_head
  
  def _get_height(self, node):
    if node is None:
      return 0
    return node.height

  # In order traversal here is used to get the sorted string 
  def inorder(self):
    return self._inorder(self.root)

  def _inorder(self, root):
    if root:
      yield from self._inorder(root.left)
      yield root 
      yield from self._inorder(root.right)

  def __len__(self):
    return self._len(self.root)

  def _len(self, root):
    if root is None:
      return 0
    return 1 + self._len(root.left) + self._len(root.right)

class Node:
  """ Node class for a tree. 
  According to the LSM Architecture, we will assume that the key is of int with value of a fixed length string.
  """
  def __init__(self, key, value="node content created"):
    self.height = 1
    self.key = key
    self.value = value + str(key)
    self.right = None 
    self.left = None 

  def __str__(self):
    return f"Key: {self.key} with value {self.value}"

if __name__ == "__main__":
  print("--- Testing AVL Tree ---") 
  avl_tree = AVL_Tree()
  avl_tree.insert(Node(10))
  avl_tree.insert(Node(9))
  avl_tree.insert(Node(8))
  avl_tree.insert(Node(7))

  print("--- Inorder traversal ---")
  # print(str(avl_tree.search(100)))
  for node in avl_tree.inorder():
    print(node)

  print("--- Testing bloom filter using Search ---")
  print(avl_tree.search(5))
  print(avl_tree.search(100))
  print(avl_tree.search(2))
  print(avl_tree.search(3))