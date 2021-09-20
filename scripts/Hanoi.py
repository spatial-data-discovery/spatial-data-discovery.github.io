import time
from Stack import Stack

def Hanoi_rec(n, s, a, d):
  print(n, s, a, d)
  # TODO replace pass with your base and recursive cases.
  if n == 0:
    d.push(s.pop())
  else:
    Hanoi_rec(n-1,s,d,a)
    d.push(s.pop())
    Hanoi_rec(n-1,a,s,d)
  print(n, s, a, d)
  print()

def Hanoi(n):
  source = Stack()
  dest = Stack()
  aux = Stack()
  i = n-1
  while i >= 0:
    source.push(i)
    i = i - 1
  Hanoi_rec(n-1, source, aux, dest)

if __name__ == '__main__':
  start = time.process_time()
  n = int(input("how many rings? "))
  Hanoi(n)
  end = time.process_time()
  print('computed Hanoi(' + str(n) + ') in ' + str(end - start) + ' seconds.')
