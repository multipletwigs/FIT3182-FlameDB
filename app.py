from LSMTree.AVLTree import AVL_Tree, Node
from LSMTree.SSTable import SSTable
from LSMTree.LevelManager import LevelManager
from LSMTree.BloomFilter import BloomFilter
import shutil 
import argparse
import os
import random

def clear_harddisk():
  if os.path.exists('./harddisk'):
    shutil.rmtree('./harddisk') 

def LSM_Execute(gls, pause_level):

  # Create harddisk directory if it doesn't exist
  if not os.path.exists('./harddisk'): 
    os.mkdir('./harddisk')

  # Initialize 3 levels 
  level_1 = LevelManager(level=1, max_size=5)  # Houses 5 sstables 
  level_2 = LevelManager(level=2, max_size=10) # Houses 10 sstables 
  level_3 = LevelManager(level=3, max_size=15) # Houses 15 sstables

  # Random unique insert workload
  insert_workload = random.sample(range(1, 100000), 2000)

  # This inserts to level 0, and flushes to level 1
  def level_0_flush():
    # Initialize memtable, this is level 0
    memtable = AVL_Tree() 
    group = 0
    # Insert workload into memtable 
    for item in insert_workload:
      # When the memtable is full, flush to disk 
      if memtable.memtable_is_full():
        # Create new sstable
        group += 1
        sstable = SSTable(level=1, group=group) 

        # This is a level 1 flush 
        sstable.write_sstable_from_memtable(memtable)

        # Initialize new memtable tree after flushing
        memtable = AVL_Tree()

        # Add sstable to level 1 
        level_1.add_sstable(sstable) 
      
      memtable.insert(Node(item))


  # Flushes from level 1 to level 2
  def level_1_flush():
    # If level 1 is full, flush to level 2
    if level_1.level_is_full(): 
      # The way GLS does it is read everything in level 1 into buffer, k-way merge the sstable, and write to level 2
      if gls:
        level_1.gls_merge(level_2) 

  # Flushes from level 2 to level 3  
  def level_2_flush():
    # If level 2 is full, flush to level 3
    if level_2.level_is_full():
      # The way GLS does it is read everything in level 2 into buffer, k-way merge the sstable, and write to level 3
      if gls:
        level_2.gls_merge(level_3)
  
  executes = [level_0_flush, level_1_flush, level_2_flush]

  # Execute the flushes up to the pause level 
  for level in range(pause_level + 1):
    func = executes[level] 
    func() 
      
if __name__=="__main__":
  # If remove harddisk flag is set, remove the harddisk
  parser = argparse.ArgumentParser(prog="LSM") 
  subparsers = parser.add_subparsers(dest='command') 

  structure_modifier_parser = subparsers.add_parser('harddisk') 
  structure_modifier_parser.add_argument('--remove-harddisk', action='store_true')

  lsm_execute = subparsers.add_parser('lsm-execute')  
  lsm_execute.add_argument('--gls', action='store_true', default=False) 
  lsm_execute.add_argument('--pause-stage', type=int, choices=[0,1,2], default=1) 

  args = parser.parse_args()

  if args.command == 'harddisk':
    if args.remove_harddisk:
      print("---- Clearing your harddisk ----")
      clear_harddisk() 
  
  elif args.command == 'lsm-execute':
    if args.gls:
      print("---- Using GLS ----")
      level = args.pause_stage
      LSM_Execute(gls=args.gls, pause_level=args.pause_stage)

  
