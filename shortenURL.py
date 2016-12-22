import random

"""
Class ShortenURL stores the input url in an array (or db) and converts its corresponding index
(or id) into a base62(10 + 26 + 26) string. The conversion to base62 is invertible, thus
facilitating retrieval (conversion is bijective).

ShortenURL.toBase62() converts base10(numvers) to base62(string)
ShortenURL.toBase10() converts base62(string) to base10(numvers)
"""

_listURL = ['' for _ in range(100000)]
_empty_indexes = random.sample(range(100000), 100000)
_characters = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_base = 62

def toBase62(base10):
    base62 = ''
    while(base10 > 0):
        base62 = _characters[base10 % _base] + base62
        base10 //= _base
    return base62

def toBase10(base62):
    base10 = 0
    for character in base62:
        base10 = _characters.index(character) + _base * base10
    return base10

def genrateIndex():
    return _empty_indexes.pop()

def shorten(url):
    index = genrateIndex()
    _listURL[index] = url
    return toBase62(index)

def lengthen(ID):
    index = toBase10(ID)
    return _listURL[index]


if __name__ == "__main__":
    str1 = shorten('http://www.billboard.com/charts/hot-100')
    print('http://www.billboard.com/charts/hot-100 shortened to: ' + str1)
    str2 = lengthen(str1)
    print(str1 + ' lengtens to: ' + str2)
    urls = [line.strip('\n') for line in open('urls.txt')]
    for url in urls:
        shorten(url)
