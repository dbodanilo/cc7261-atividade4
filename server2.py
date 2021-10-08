
import sympy
import socket
import concurrent.futures

from time import perf_counter_ns
from primes import *


def evaluation(cod, n):
  start = perf_counter_ns()

  primes_cod = primes(cod + 1)

  with concurrent.futures.ThreadPoolExecutor() as executor:
    future_ant = executor.submit(check_backward, n, primes_cod)
    future_pos = executor.submit(check_forward, cod, n, primes_cod)

    left = future_ant.result()
    right = future_pos.result()
 
    code = left * right

    end = perf_counter_ns()
    t = (end - start) / 1000000

    #print(f"left: {left}")
    #print(f"right: {right}")
    #print(f"code: {code}")
    #print(f"{t:.2f}ms")

    return code       


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('localhost', 50023))
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

        #Evalutation
        key = evaluation(cod, n)
        
        response = f'{key}'  
        b_response = bytes(response, 'utf-8')
        conexao.sendall(b_response)
