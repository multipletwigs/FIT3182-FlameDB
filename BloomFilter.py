from bitarray import bitarray

""" Small scale bloom filter
1. It takes in the number of elements that you're planning to store
2. From there, based on a particular error rate, determine size of hash_table
3. Citation: https://stackoverflow.com/questions/658439/how-many-hash-functions-does-my-bloom-filter-need
"""
class BloomFilter:
  def __init__(self, size=100000, avg_bits=4):
    self.hash_table = [0] * size
    self.avg_bits = avg_bits 
  
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
  bf = BloomFilter()
  bf.insert("hello")
  bf.insert("world")
  print(bf.membership_check("hello", debug=True))
  print(bf.membership_check("world", debug=True))
  print(bf.membership_check("hello world", debug=True))

  

