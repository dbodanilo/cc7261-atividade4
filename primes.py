from primesieve.numpy import primes, n_primes


def check_backward(primes_cod, n):
  return primes_cod[-n]


def check_forward(nprimes_cod, n):
  nprimes = nprimes_cod + n

  primes_top = n_primes(nprimes)

  return primes_top[nprimes - 1]

