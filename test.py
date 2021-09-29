import sympy

from time import perf_counter_ns

num_primes = [0]

def check_inputs(cod, n):
    x = min(len(num_primes) - 1, cod)
 
    primes = num_primes[x]
    while x <= cod:
        if x >= len(num_primes):
            num_primes.append(primes)

            if sympy.isprime(x):
                primes += 1
        x += 1

    return cod > 1000000 and num_primes[cod] >= 2*n

start = perf_counter_ns()

check_inputs(1000001, 1000)

end = perf_counter_ns()
print(f"first: {(end - start)/1000} ms")

start = perf_counter_ns()

check_inputs(1001000, 1000)

end = perf_counter_ns()
print(f"second: {(end - start)/1000} ms")
