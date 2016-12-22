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
"""

import time
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
        self.versions = versions
        self.hash = [[] for x in range(103)]
        # hash with 100 buckets

    def hash_function(self, key):
        # calculate index
        index = toBase10(key) % 103
        return index

    def getWord(self, index_bucket, key):
        for word in self.hash[index_bucket]:
            if word.key == key:
                return word
        return False

    def add(self, key, value):
        index_bucket = self.hash_function(key)
        word = self.getWord(index_bucket, key)
        if not word:
            word = Word(key, self.versions)
            self.hash[index_bucket].append(word)
        word.valueQ.push(value)

    def get(self, key, version = 0):
        index_bucket = self.hash_function(key)
        word = self.getWord(index_bucket, key)
        if word:
            element = word.valueQ.get(version)
            print(element.value, element.timestamp)
            return element
        else:
            print('Key does not exist!')
            return 0






