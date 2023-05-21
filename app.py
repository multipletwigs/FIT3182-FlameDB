if __name__ == "__main__":

  # Initialize memtable
  memtable = AVL_Tree() 

  # Initialize 3 levels 
  level_1 = LevelManager(level=0, max_size=5)  # Houses 5 sstables 
  level_2 = LevelManager(level=1, max_size=10) # Houses 10 sstables 
  level_3 = LevelManager(level=2, max_size=15) # Houses 15 sstables

  # Initialize insert workload 
  insert_workload = [i for i in range(1000)] 

  # Initialize search workload
  search_workload = [i for i in range(1000, 2000)]

  # Insert workload into memtable
  
