from bitarray import bitarray

""" Small scale bloom filter
1. It takes in the number of elements that you're planning to store
2. From there, based on a particular error rate, determine size of hash_table
3. Citation: https://stackoverflow.com/questions/658439/how-many-hash-functions-does-my-bloom-filter-need
"""
class BloomFilter:
  def __init__(self, size=100):
    self.hash_table = [0] * size
  
  def _hash_gen(self):
    pass 
  
  def insert(self, key):
    # 1. Hash Key

    # 2. Insert to hash table
    pass 

  def membership_check(self, key):
    # 1. Hash key

    # 2. Check if maybe in hash table

    # 3. return True if maybe in, False if not
    pass 

  

