class BloomFilter:

  def __init__(self, level, hobf=False):

    # Mapping of level to size of hash table, 
    # using the heterogenous bloom filters
    SIZE_MAPPING = {
        0: 100000,
        1: 10000,
        2: 1000,
      }

    # If using homogenous bloom filters, 
    # all levels have the same size
    if hobf:
      SIZE_MAPPING = {
          0: 1000,
          1: 1000,
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

  

