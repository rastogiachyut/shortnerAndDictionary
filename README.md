# shortnerAndDictionary
Python program for a url shortner and an implementation of dictionary 

Instructions to run:
1) The URL Shortener is a module, so either copy the file to a folder
that is added to your python path or clone the repo add it to your
python paths.
2) The Dictionary uses the shortenURL module, so please check that the
module is availble(not problem if you've used the shortenURL module).
3) Python 3.5.2 [GCC 5.4.0 20160609] on linux was used to write this
code.

Limitations:

1)URL shortener
- It can handle a max of 100000 urls only.
- No regex has been added to check for urls only.

2)Dictionary
- The keys can only be composed of the 62 characters, i.e. numbers +
small alphabets + acpital alphabets.
- The hashing is relatively simple and collisions are simply handled
by extending the buckets, better techniques can be used if the type
of keys or use of dictionary are known.
- The get function returns a object of type element, element has two
attributes, value and timestamp. It also prints these values.
