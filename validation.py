import sympy

def check_inputs(cod, n):

    """ def input_function(msg=None):
        try:
            r = int(input(msg))
            return r
        except:
            print("Not an int")
            return input_function(msg) """

    primes = 0
    x = cod
    while primes < 2*n and x > 0:
        if sympy.isprime(x):
            primes += 1
        x -= 1

    if cod >= 1000000 and n*2 <= primes:
        return True
    else:
        return False




b = check_inputs(1000234, 10000)

print(b)


