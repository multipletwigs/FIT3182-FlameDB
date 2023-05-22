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


def initialize_app(max_size=100, size_multiple=5, hobf=True, search_size=100):
    random.seed(42)

    # Create harddisk directory if it doesn't exist
    if not os.path.exists('./harddisk'):
        os.mkdir('./harddisk')

    # Initialize 2 levels with 1 memtable
    memtable = AVL_Tree(hobf=hobf)
    level_1 = LevelManager(level=1, max_size=max_size, hobf=hobf)
    level_2 = LevelManager(level=2, max_size=max_size * size_multiple, hobf=hobf)

    # Insert workload, here * 100 is because SSTables are 100 in size by default
    insert_workload = [Node(i) for i in range((max_size * 100 + max_size *
                                               size_multiple * 100) - random.randint(max_size, max_size * size_multiple))]
    search_workload = random.sample(insert_workload, 1000)
    return memtable, level_1, level_2, insert_workload, search_workload


def LSM_Insert(gls, max_size, size_multiple, hobf=True, benchmark=True):

    memtable, level_1, level_2, insert_workload, search_workload = initialize_app(max_size=max_size, size_multiple=size_multiple)
    total_memtable_size = 0
    total_buffer_used = 0
    total_insert_size = sys.getsizeof([str(node) for node in insert_workload])
    total_search_size = sys.getsizeof([str(node) for node in search_workload])
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

            sstable = SSTable(level=1, group=group, hobf=hobf)

            group += 1

            # Add to total memtable size before new memtable
            total_memtable_size += memtable.total_bytes()

            # This is a level 1 flush
            sstable.write_sstable_from_memtable(memtable)

            # Initialize new memtable tree after flushing
            memtable = AVL_Tree(hobf=hobf)

            # Add sstable to level 1
            level_1.add_sstable(sstable)

    # Benchmarking search
    total_search_buffer_used = 0
    for node in search_workload:
        results = memtable.search(node)
        if not results:
            results, buffer_used = level_1.search_level(node)
            total_search_buffer_used += buffer_used
            if not results:
                results, buffer_used = level_2.search_level(node)
                total_search_buffer_used += buffer_used

    if benchmark:
        # Write workload measurement for disk amplification
        print("-- Benchmarking Insert --")
        print(f"Total buffer used: {total_buffer_used / 1000000} MB")
        print(f"Total Workload Size: {total_insert_size / 1000000} MB")
        print(f"Disk Amplification: {(total_buffer_used) / total_insert_size}\n")
        return total_buffer_used / total_insert_size


        # Search workload for the write workload 
        print("-- Benchmarking Search --")
        print(f"Total buffer used: {total_search_buffer_used  / 1000000} MB")
        print(f"Total Workload Size: {total_search_size / 1000000} MB")
        print(f"Disk Amplification: {(total_search_buffer_used) / total_search_size}\n")
        return total_search_buffer_used / total_search_size


if __name__ == "__main__":
    # If remove harddisk flag is set, remove the harddisk
    parser = argparse.ArgumentParser(prog="LSM")
    MAX_SIZE = 100
    SIZE_MULTIPLE = 5

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
        print(
            f"---- Running benchmark for GLS where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=True, benchmark=True, max_size=MAX_SIZE,
                   size_multiple=SIZE_MULTIPLE)

        print(
            f"---- Running benchmark for traditional LSM where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=False, benchmark=True, max_size=MAX_SIZE,
                   size_multiple=SIZE_MULTIPLE)

    elif args.gls:
        print(
            f"---- Running GLS where Level 1: {MAX_SIZE} and Level 2: {MAX_SIZE * SIZE_MULTIPLE} ----")
        LSM_Insert(gls=True, benchmark=False, max_size=MAX_SIZE,
                   size_multiple=SIZE_MULTIPLE)
