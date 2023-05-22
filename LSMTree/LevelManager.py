from LSMTree.SSTable import SSTable
import os

class LevelManager:
  def __init__(self, level, max_size):
    self.sstable_list = []
    self.level = level
    self.directory = f'./harddisk/level_{self.level}'
    self.size = 0
    self.max_size = max_size

    # Create directory if it doesn't exist
    if not os.path.exists(self.directory):
      os.mkdir(self.directory)

  """
  Merges into the new level if the level is full, this compaction is called Grouped Level Structure
  """
  def gls_merge(self, next_level_manager):
    # Read all sstables into buffer 
    buffer = set() 
    for sstable in self.sstable_list:

      # A set is used here to remove duplicates! 
      # Compaction states we should remove duplicates, 
      # and the last sstable in the list is the most recent 
      for item in sstable.read_sstable():
        buffer.add(item)

    # Sort the buffer based on a split key 
    buffer = list(buffer)
    buffer.sort(key=lambda x: int(x.split('|')[0])) 

    # Merge the buffer into a new sstable
    group = 0
    sstable = SSTable(level=self.level + 1, group=group) 

    # Based on the whole buffer, split into appropriate sstables and groups if the SSTable is already full 
    for item in buffer:
      if sstable.sstable_is_full():
        # Add to the level if it is already full 
        next_level_manager.add_sstable(sstable)

        # Switch to a new group
        group += 1

        # Create a new sstable 
        sstable = SSTable(level=self.level + 1, group=group)

      sstable.write_to_sstable({
        'key': int(item.split('|')[0]),
        'value': item.split('|')[1]
      }) 

    # After flushing the buffer to the next level, clear the sstables in the current level 
    self.purge_level()

  def trad_merge(self, next_level_manager):
    # Read all sstables into buffer, both levels
    buffer = set()
    for sstable in self.sstable_list:
      for item in sstable.read_sstable():
        buffer.add(item)

    for sstable in next_level_manager.get_sstable_list():
      for item in sstable.read_sstable():
        buffer.add(item)

    # Sort the buffer based on a split key
    buffer = list(buffer)
    buffer.sort(key=lambda x: int(x.split('|')[0]))

    # Merge the buffer into a new sstable
    group = 0
    sstable = SSTable(level=self.level + 1, group=group)

    # Based on the whole buffer, split into appropriate sstables and groups if the SSTable is already full
    for item in buffer:
      if sstable.sstable_is_full():
        # Add to the level if it is already full
        next_level_manager.add_sstable(sstable)

        # Switch to a new group
        group += 1

        # Create a new sstable
        sstable = SSTable(level=self.level + 1, group=group)

      sstable.write_to_sstable({
        'key': int(item.split('|')[0]),
        'value': item.split('|')[1]
      })

    # After flushing the buffer to the next level, clear the sstables in the current level
    self.purge_level()

  def purge_level(self):
    self.sstable_list = []
    self.size = 0

    for file in os.listdir(self.directory):
      os.remove(os.path.join(self.directory, file))
    
  def add_sstable(self, sstable):
    self.sstable_list.append(sstable)  
    # Add to the directory as well 

    self.size += 1

  def get_sstable(self, index):
    return self.sstable_list[index]

  def get_sstable_list(self):
    return self.sstable_list

  def level_is_full(self):
    return self.size >= self.max_size

  