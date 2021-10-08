import socket

from concurrent.futures import ThreadPoolExecutor
from time import perf_counter_ns
from primes import *


def evaluation(cod, n):
  primes_cod = primes(cod)

  with ThreadPoolExecutor() as executor:
    future_ant = executor.submit(check_backward, n, primes_cod)
    future_pos = executor.submit(check_forward, cod, n, primes_cod)

    left = future_ant.result()
    #print(f"left: {left}")

    right = future_pos.result()
    #print(f"right: {right}")
 
    code = left * right

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
        start = perf_counter_ns()

        key = evaluation(cod, n)

        end = perf_counter_ns()
        # ms from ns
        t = (end - start) / 1e6
        #print(f"{t:.2f}ms")
        
        response = f'{key}'  
        #print("code: ", response)
        b_response = bytes(response, 'utf-8')
        conexao.sendall(b_response)
