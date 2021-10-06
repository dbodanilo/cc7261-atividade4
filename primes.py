
from sympy import isprime

import numpy


def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n//3 + (n%6==2), dtype=numpy.bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]


num_primes = [0]

def primes(n):
    """ Returns  a list of primes < n """
    sieve = [True] * n
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i]:
            sieve[i*i::2*i]=[False]*((n-i*i-1)//(2*i)+1)
    return [2] + [i for i in range(3,n,2) if sieve[i]]


def check_inputs(cod, n):
    return cod > 1000000 and len(primesfrom2to(cod)) >= 2 * n


def check_backward(cod, n):
  primes_cod = primesfrom2to(cod)
  
  return primes_cod[-n]


def check_forward(cod, n):
  top = 3 * n
  primes_cod = primesfrom2to(cod + top)

  while len(primes_cod[(cod + 1):]) < n:
    top *= 2 
    primes_cod = primesfrom2to(cod + top)
  
  return primes_cod[n]


def eval_backward(cod, n):
  i = 0
  ant = cod
  while(i < n):
    ant -= 1
    if isprime(ant):
      i += 1
  return ant

def eval_forward(cod, n):
  i = 0
  pos = cod
  while(i < n):
    pos += 1
    if isprime(pos):
      i += 1
  return pos

