#!/usr/bin/env python

# Edited to refernce file in data folder

fhand = open('data/mbox-short.txt')
for line in fhand:
    line = line.rstrip()
    if not line.startswith('From '): continue
    words = line.split()
    print(words[2])
