class SSTable:
  def __init__(self, tree, level, group):
    self.AVLTree = tree
    self.level = level
    self.group = group
    self.path = f'./level/{self.level}/SSTable_{self.level}{self.group}.sst'

  def write_sstable(self):

    # Create group directory if it doesn't exist
    if not os.path.exists(f'./level/{self.level}'):
      os.mkdir(f'./{self.level}')

    # Write to the particular group
    with open(f'./level/{self.level}/SSTable_{self.level}{self.group}.sst', 'w') as f:
      generator = self.AVLTree.inorder()
      for node in generator:
        f.write(f"{node.key} {node.value}\n")

  def seach_sstable(self, key):
    # Load the SSTable into memory and search for the key using binary search
    with open(f'./level/{self.level}/SSTable_{self.level}{self.group}.sst', 'r') as f:
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
      if int(lines[mid].split()[0]) == key:
        return lines[mid].split()[1]
      elif int(lines[mid].split()[0]) < key:
        left = mid + 1
      else:
        right = mid - 1
    return None

  
    
