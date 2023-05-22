from LSMTree.AVLTree import AVL_Tree, Node
from LSMTree.BloomFilter import BloomFilter
import os

class SSTable:
  def __init__(self, level, group):
    self.level = level
    self.group = group
    self.max_elements = 100
    self.num_elements = 0
    self.bloomFilter = BloomFilter(self.level) 
    self.level_path = f'./harddisk/level_{self.level}'
    self.file_path = f'./harddisk/level_{self.level}/SSTable_{self.level}{self.group}.sst'

  def read_sstable(self):
    with open(self.file_path, 'r') as f:
      lines = f.readlines()
      return lines

  def write_sstable_from_memtable(self, memtable):
    # Create group directory if it doesn't exist
    if not os.path.exists(self.level_path):
      os.mkdir(self.level_path)

    # Writing from memtable to SSTable 
    with open(self.file_path, 'w') as f:
      generator = memtable.inorder()
      for node in generator:
        f.write(f"{node.key}|{node.value}\n")
        self.num_elements += 1
        self.bloomFilter.insert(node.key)

  # K-way merge ensures that writing to sstable is in order. 
  def write_to_sstable(self, kv):
    with open(self.file_path, 'w') as f:
      self.num_elements += 1
      self.bloomFilter.insert(kv['key'])
      f.write(f"{kv['key']}|{kv['value']}\n")

  # If the sstable is full, the manager should create a new sstable and continue writing to the other sstable
  def sstable_is_full(self):
    return self.num_elements >= self.max_elements 

  def search_sstable(self, key):

    # Check if the key is in the bloom filter
    if not self.bloomFilter.membership_check(key):
      raise KeyError(f"Key {key} not found in SSTable. Bloom Filter says so.")

    # Load the SSTable into memory and search for the key using binary search 
    with open(self.file_path, 'r') as f:
      lines = f.readlines()

      # If the binary search returns None, means nothing was found
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
  memtable = AVL_Tree() 
  # Random array of 1000 elements with no repeats
  arr = [random.randint(0, 5000) for _ in range(1000)] 
  for i in arr:
    memtable.insert(Node(i))

  sstable = SSTable(level=0, group=0)
  sstable.write_sstable_from_memtable(memtable)


  
    
