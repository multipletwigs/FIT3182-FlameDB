from LSMTree.AVLTree import AVL_Tree, Node
from LSMTree.SSTable import SSTable
from LSMTree.LevelManager import LevelManager
from LSMTree.BloomFilter import BloomFilter
import shutil
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
    level_2 = LevelManager(level=2, max_size=max_size *
                           size_multiple, hobf=hobf)

    # Insert workload, here * 100 is because SSTables are 100 in size by default
    insert_workload = [Node(i) for i in range((max_size * 100 + max_size *
                                               size_multiple * 100) - random.randint(max_size, max_size * size_multiple))]
    search_workload = random.sample(insert_workload, 1000)
    return memtable, level_1, level_2, insert_workload, search_workload

def LSM_Insert(gls, max_size, size_multiple, hobf=True, benchmark=True):

    memtable, level_1, level_2, insert_workload, search_workload = initialize_app(
        max_size=max_size, size_multiple=size_multiple)
    total_memtable_size = 0
    total_buffer_used = 0
    total_insert_size = sys.getsizeof([str(node) for node in insert_workload])
    total_search_size = sys.getsizeof([str(node) for node in search_workload])
    group = 0

    # Insert workload into memtable
    print("Now Inserting...")
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
    print("Finished inserting! ...")

    # Benchmarking search
    print("Now searching...")
    total_search_buffer_used = 0
    for node in search_workload:
        results = memtable.search(node)
        if not results:
            results, buffer_used = level_1.search_level(node)
            total_search_buffer_used += buffer_used
            if not results:
                results, buffer_used = level_2.search_level(node)
                total_search_buffer_used += buffer_used

    print("Finished searching! ...")

    if benchmark:
        # Write workload measurement for disk amplification
        print("-- Benchmarking Insert --")
        print(f"Total buffer used: {total_buffer_used / 1000000} MB")
        print(f"Total Workload Size: {total_insert_size / 1000000} MB")
        print(
            f"Disk Amplification: {(total_buffer_used) / total_insert_size}\n")
        insert_amp = total_buffer_used / total_insert_size

        # Search workload for the write workload
        print("-- Benchmarking Search --")
        print(f"Total buffer used: {total_search_buffer_used  / 1000000} MB")
        print(f"Total Workload Size: {total_search_size / 1000000} MB")
        print(
            f"Disk Amplification: {(total_search_buffer_used) / total_search_size}\n")
        search_amp = total_search_buffer_used / total_search_size

        return insert_amp, search_amp, total_insert_size, total_buffer_used, total_search_size, total_search_buffer_used
