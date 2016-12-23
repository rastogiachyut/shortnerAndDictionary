"""
Design:
I am using a list of lists to create a key value data-store.
Its structure will be as such:
[ # This list contains many buckets(pages)
    [ # Each bucket has many (words)[key, Queue object] pairs
        [key1, valueQ1], # Queue object store the multiple versions of a value
        [key2, valueQ2]  # and timestamp
    ],
    [
        [key3, valueQ3],
        [key4, valueQ4],
        [key5, valueQ5]
    ]
]

word: is [key, valueQ]
    entry.key = key
    entry.valueQ = valueQ

element: is [value1, timestamp]
    element.value = value
    element.tmestamp = timestamp

The steps for adding are:
1)Get index from hash function.
2)Create word and add to calculated bucket if key is new else get old word and
push in new value version.
3)Check load, rehash if needed.

The steps for getting are:
1)Get index from hash function.
2)Get word from bucket, O(bucket_size)
3)Return word
"""

import time
import math
import datetime
from shortenURL import toBase10

class Element:

    def __init__(self, value):
        self.value = value
        self.timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d/%m/%Y %H:%M:%S')


class ValueQ:

    def __init__(self, limit):
        self.queue = []
        self.limit = limit
        
    def push(self, value):
        if len(self.queue) >= self.limit:
            del self.queue[0]
        self.queue.append(Element(value))

    def get(self, version):
        if version >= self.limit:
            print('You have exceeded the version limit')
            return False
        return self.queue[-(1 + version)]


class Word:

    def __init__(self, key, limit):
        self.key = key
        self.valueQ = ValueQ(limit)


class Dictionary:

    def __init__(self, versions):
        self.size = 3
        # not a realistic size to start from but better for testing
        self.load = 0
        self.versions = versions
        self.hash = [[]] * self.size
        # hash with 103 buckets

    def is_prime(self, n):
        if n % 2 == 0 and n > 2:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True

    def next_prime(self, currentPrime):
        new_size = 2 * currentPrime
        while not self.is_prime(new_size):
            new_size += 1
        return new_size

    def add_word(self, word):
        index_bucket = self.hash_function(word.key)
        self.hash[index_bucket].append(word)

    def hash_function(self, key):
        index = toBase10(key) % self.size
        return index

    def rehash(self):
        # Used when load_factor is 0.7 or more
        self.size = self.next_prime(self.size)
        old_hash = self.hash
        self.hash = [[]] * self.size
        for bucket in old_hash:
            for word in bucket:
                self.add_word(word)

    def check_load(self):
        if self.load/self.size >= 0.7:
            self.rehash()

    def get_word(self, index_bucket, key):
        for word in self.hash[index_bucket]:
            if word.key == key:
                return word
        return False

    def add(self, key, value):
        index_bucket = self.hash_function(key)
        word = self.get_word(index_bucket, key)
        if not word:
            word = Word(key, self.versions)
            self.hash[index_bucket].append(word)
        word.valueQ.push(value)
        self.load += 1
        self.check_load()

    def get(self, key, version = 0):
        index_bucket = self.hash_function(key)
        word = self.get_word(index_bucket, key)
        if word:
            element = word.valueQ.get(version)
            print(element.value, element.timestamp)
            return element
        else:
            print('Key does not exist!')
            return 0


if __name__ == "__main__":
    d = Dictionary(2)
    print(len(d.hash))
    d.add('q', 12)
    d.add('q', 34)
    d.add('w', 13)
    d.add('e', 14)
    print(len(d.hash))
    d.get('q')
    d.get('w')
    d.get('e')


