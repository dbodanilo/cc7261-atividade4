import socket
import sympy
#from validation import check_inputs

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


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('127.0.0.1', 50002))
  print(s)
  while True:
    s.listen()
    conexao, addr = s.accept()
    with conexao:
      print(f"Cliente conectado: {addr}")
      while True:
        dados = conexao.recv(1024)
        if not dados:
          break
        print(f"Código inicial: {eval(dados.decode())[0]}")
        print(f"n: {eval(dados.decode())[1]}")

        cod = eval(dados.decode())[0]
        n = eval(dados.decode())[1]

        #Communication with server 2
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
          if check_inputs(cod, n):
            c.connect(("127.0.0.1", 50003))
            print(c)
            msg = f"{cod}, {n}"
            b_string = bytes(msg, 'utf-8')
            c.sendall(b_string)
            dados = c.recv(1024)
            print(f"Resposta do servidor: {dados.decode()}")
            
            response = str(dados.decode())
            b_response = bytes(response, 'utf-8')
          else:
            b_response = b'Invalid Inputs'
            
        conexao.sendall(b_response)