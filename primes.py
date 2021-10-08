

import numpy

from sympy import isprime
from scipy.special import lambertw
from math import exp


def primes(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n//3 + (n%6==2), dtype=numpy.bool)
    for i in range(1,int(n**0.5)//3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k//3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)//3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]


def check_backward(n, primes_cod):
  return primes_cod[-n]


def check_forward(cod, n, primes_cod):
  n0 = len(primes_cod) - 1
  n2 = n0 + n

  top = int (cod/n0 * (n0 + n))

  primes_top = primes(top)

  while len(primes_top) < n:
    top *= 2 
    #print("short list")
    primes_top = primes(top + 1)
  
  return primes_top[n]


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

