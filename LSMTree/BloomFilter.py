from bitarray import bitarray

""" Small scale bloom filter
1. It takes in the number of elements that you're planning to store
2. From there, based on a particular error rate, determine size of hash_table
3. Citation: https://stackoverflow.com/questions/658439/how-many-hash-functions-does-my-bloom-filter-need
"""
class BloomFilter:

  def __init__(self, level):

    # Mapping of level to size of hash table
    SIZE_MAPPING = {
        0: 100000,
        1: 10000,
        2: 1000,
      }

    # The upper the component, the more bits that the hash table is assigned to
    self.hash_table = [0] * SIZE_MAPPING[level]

    # For comparison, all levels are assigned 4 bits
    self.avg_bits = 4
  
  def insert(self, key):
    for i in range(self.avg_bits):
      hash_val = hash(key) % len(self.hash_table)
      self.hash_table[hash_val] = 1

  def membership_check(self, key, debug=False):
    for i in range(self.avg_bits):
      hash_val = hash(key) % len(self.hash_table)
      if self.hash_table[hash_val] == 0:
        if debug:
          print(f"Key {key} is not in bloom filter.")
        return False

    if debug:
      print(f"Key {key} is potentially in bloom filter.")
    return True

if __name__ == "__main__":
  bf = BloomFilter(0)
  bf.insert("hello")
  bf.insert("world")
  print(bf.membership_check("hello", debug=True))
  print(bf.membership_check("world", debug=True))
  print(bf.membership_check("hello world", debug=True))

  
