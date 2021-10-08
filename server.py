import socket
import sympy
from time import perf_counter_ns

from primes import *


def check_inputs(cod, n):
  start = perf_counter_ns()
 
  ok = cod > 1000000 and len(primes(cod)) >= 2 * n
  
  end = perf_counter_ns()

  #print("valid" if ok else "invalid", " input")
  t = (end - start) / 1000000
  #print(f"{t:.2f}ms")

  return ok


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('localhost', 50022))
  print(s)
  while True:
    s.listen()
    conexao, addr = s.accept()
    with conexao:
      #print(f"Cliente conectado: {addr}")
      while True:
        dados = conexao.recv(1024)
        if not dados:
          break
        #print(f"Código inicial: {eval(dados.decode())[0]}")
        #print(f"n: {eval(dados.decode())[1]}")

        cod = eval(dados.decode())[0]
        n = eval(dados.decode())[1]

        #Communication with server 2
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
          if check_inputs(cod, n):
            c.connect(("127.0.0.1", 50023))
            #print(c)
            msg = f"{cod}, {n}"
            b_string = bytes(msg, 'utf-8')
            c.sendall(b_string)
            dados = c.recv(1024)
            #print(f"-->{dados.decode()}")
            
            response = str(dados.decode())
            b_response = bytes(response, 'utf-8')
          else:
            b_response = b'Invalid Inputs'
            
        conexao.sendall(b_response)
