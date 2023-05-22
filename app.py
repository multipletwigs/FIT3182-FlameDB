from LSMTree.AVLTree import AVL_Tree, Node
from LSMTree.SSTable import SSTable
from LSMTree.LevelManager import LevelManager
from LSMTree.BloomFilter import BloomFilter
import shutil
import psutil
import argparse
import os
import random
import sys


def clear_harddisk():
    if os.path.exists('./harddisk'):
        shutil.rmtree('./harddisk')


def initialize_app():
    random.seed(42)

    # Create harddisk directory if it doesn't exist
    if not os.path.exists('./harddisk'):
        os.mkdir('./harddisk')

    # Initialize 2 levels with 1 memtable
    memtable = AVL_Tree()
    level_1 = LevelManager(level=1, max_size=10)
    level_2 = LevelManager(level=2, max_size=30)

    # Insert workload
    insert_workload = [Node(i) for i in range(2500)]
    return memtable, level_1, level_2, insert_workload


def LSM_Execute(gls, benchmark=True):

    memtable, level_1, level_2, insert_workload = initialize_app()
    total_memtable_size = 0
    total_buffer_used = 0
    total_workload_size = sys.getsizeof(
        [str(node) for node in insert_workload])
    group = 0

    # Insert workload into memtable
    for idx, node in enumerate(insert_workload):
        memtable.insert(node)
        if memtable.memtable_is_full():
            if level_1.level_is_full():
                # Just did a flush so the group now goes back to 0
                if gls:
                    total_buffer_used += level_1.gls_merge(level_2)
                    group = 0
                else:
                    total_buffer_used += level_1.trad_merge(level_2)
                    group = 0

            sstable = SSTable(level=1, group=group)

            group += 1

            # Add to total memtable size before new memtable
            total_memtable_size += memtable.total_bytes()

            # This is a level 1 flush
            sstable.write_sstable_from_memtable(memtable)

            # Initialize new memtable tree after flushing
            memtable = AVL_Tree()

            # Add sstable to level 1
            level_1.add_sstable(sstable)

    if benchmark:
        print(f"Total buffer used: {total_buffer_used}")
        print(f"Total memtable size: {total_memtable_size}")
        return (total_buffer_used + total_memtable_size) / total_workload_size


if __name__ == "__main__":
    # If remove harddisk flag is set, remove the harddisk
    parser = argparse.ArgumentParser(prog="LSM")

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--purge', action='store_true',
                       help="Clear harddisk after execution")

    group.add_argument('--benchmark', action='store_true', default=False,
                       help="Run benchmark")

    lsm_execute = group.add_mutually_exclusive_group()
    lsm_execute.add_argument('--gls',
                             action='store_true',
                             default=False,
                             help="Use GLS compaction algorithm")

    lsm_execute.add_argument('--trad', action='store_true', default=False,
                             help="Use traditional compaction algorithm (Levels DB)")

    args = parser.parse_args()

    if args.purge:
        print("---- Clearing your harddisk ----")
        clear_harddisk()

    elif args.benchmark:
        write_amp = LSM_Execute(gls=True, benchmark=True)
        print(f"Write amplification: {write_amp}")
        write_amp = LSM_Execute(gls=False, benchmark=True)
        print(f"Write amplification: {write_amp}")

    elif args.gls:
        write_amp = LSM_Execute(gls=True, benchmark=True)
        print(f"Write amplification: {write_amp}")
