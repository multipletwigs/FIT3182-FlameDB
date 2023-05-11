class Compaction:
  def __init__(self, sstable1, sstable2):
    self.sstable1 = sstable1
    self.sstable2 = sstable2
  
  def k_way_merge(self, sstable1, sstable2):
    # Load sstable1 and sstable2 into memory
    with open(sstable1.path, 'r') as f:
      sstable1_lines = f.readlines()
    with open(sstable2.path, 'r') as f:
      sstable2_lines = f.readlines()
    
    # Merge the two sstables
    merged_sstable = self._merge(sstable1_lines, sstable2_lines)

    # Write the merged sstable to disk
    with open(f'./level/{sstable1.level}/SSTable_{sstable1.level}{sstable1.group}.sst', 'w') as f:
      for line in merged_sstable:
        f.write(line)