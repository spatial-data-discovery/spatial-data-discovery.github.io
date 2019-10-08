#!/usr/bin/env python3
import os
import string

for fname in os.listdir('.'):
  if fname.endswith('.txt', '.asc'):
    data = open(fname).readlines()

    listnum = []
    listalpha = []
    for line in data:
      line = line.strip()
      if str(line).startswith(('0,1,2,3,4,5,6,7,8,9')):
        listnum.append()
      if line[:1].isalpha():
        listalpha.append()
    print(len(listnum))

    print(len(a) == len(b))
