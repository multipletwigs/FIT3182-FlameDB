from LSMTree.AVLTree import AVL_Tree, Node
from LSMTree.SSTable import SSTable
from LSMTree.LevelManager import LevelManager
from LSMTree.BloomFilter import BloomFilter

if __name__ == "__main__":

  # Initialize memtable
  memtable = AVL_Tree() 

  # Initialize 3 levels 
  level_1 = LevelManager(level=0, max_size=5)  # Houses 5 sstables 
  level_2 = LevelManager(level=1, max_size=10) # Houses 10 sstables 
  level_3 = LevelManager(level=2, max_size=15) # Houses 15 sstables

  # Initialize insert workload 
  insert_workload = [i for i in range(1000)] 

  # Insert workload into memtable 
  for item in insert_workload:

    # When the memtable is full, flush to disk 
    if memtable.memtable_is_full():
      # Create new sstable
      sstable = SSTable(level=0, group=0) 

      # This is a level 1 flush 
      sstable.write_sstable_from_memtable(memtable)

      # Initialize new memtable tree after flushing
      memtable = AVL_Tree()

      # Add sstable to level 1 
      level_1.add_sstable(sstable) 
    
    memtable.insert(Node(item))
  
