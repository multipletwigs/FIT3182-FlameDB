class LevelManager:
  def __init__(self, level, max_size):
    self.sstable_list = []
    self.level = level
    self.directory = f'./harddisk/level_{self.level}'
    self.size = 0
    self.max_size = max_size

  def add_sstable(self, sstable):
    self.sstable_list.append(sstable)
    self.size += 1

  def get_sstable(self, index):
    return self.sstable_list[index]

  def get_sstable_list(self):
    return self.sstable_list

  def level_is_full(self):
    return self.size == self.max_size



  