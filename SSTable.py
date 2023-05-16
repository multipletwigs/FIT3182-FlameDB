from AVLTree import *
import os

class SSTable:
  def __init__(self, tree, level, group):
    self.AVLTree = tree
    self.level = level
    self.group = group
    self.level_path = f'./harddisk/level_{self.level}'
    self.file_path = f'./harddisk/level_{self.level}/SSTable_{self.level}{self.group}.sst'

  def write_sstable(self):

    # Create group directory if it doesn't exist
    if not os.path.exists(self.level_path):
      os.mkdir(self.level_path)

    # Write to the particular group
    with open(self.file_path, 'w') as f:
      generator = self.AVLTree.inorder()
      for node in generator:
        f.write(f"{node.key}|{node.value}\n")

  def search_sstable(self, key):
    # Load the SSTable into memory and search for the key using binary search
    with open(self.file_path, 'r') as f:
      lines = f.readlines()
      item = self._binary_search(lines, key)
      if item:
        return item
      else:
        raise KeyError

  def _binary_search(self, lines, key):
    left = 0
    right = len(lines) - 1
    while left <= right:
      mid = (left + right) // 2
      [ss_key, value] = lines[mid].split("|")
      if int(ss_key) == key:
        return Node(key, value)
      elif int(ss_key) < key:
        left = mid + 1
      else:
        right = mid - 1
    return None

if __name__ == "__main__":
  import random 
  avl = AVL_Tree() 
  # Random array of 1000 elements with no repeats
  arr = [random.randint(0, 5000) for _ in range(1000)] 
  for i in arr:
    avl.insert(Node(i))

  sstable = SSTable(avl, level=0, group=0)
  sstable.write_sstable()


  
    
