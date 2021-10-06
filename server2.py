
import sympy
import socket
import concurrent.futures

from time import perf_counter_ns

from primes import *


def resolve_thread(data, ThreadsQtdd):
    #ThreadsQtdd = 5
    tamanholista = len(data)
    index = range(0, tamanholista+(tamanholista//ThreadsQtdd), tamanholista//ThreadsQtdd)
    primos = 0
    #primos = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(ThreadsQtdd):
            futures.append(executor.submit(tCalculaPrimo, data=data[index[i]:index[i+1]]))
        for future in concurrent.futures.as_completed(futures):
            #futures.append(future.result())
            primos += future.result()
    return primos


def evaluation(cod, n):
  start = perf_counter_ns()

  with concurrent.futures.ThreadPoolExecutor() as executor:
    future_ant = executor.submit(check_backward, cod, n)
    future_pos = executor.submit(check_forward, cod, n)

    code = future_ant.result() * future_pos.result()

    end = perf_counter_ns()

    t = (end - start) / 1000000

    print("{:.2f}ms".format(t))

    return code       


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('localhost', 50023))
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
        """ print(f"Código inicial: {eval(dados.decode())[0]}")
        print(f"n: {eval(dados.decode())[1]}") """

        cod = eval(dados.decode())[0]
        n = eval(dados.decode())[1]

        #Evalutation
        key = evaluation(cod, n)
        
        response = f'{key}'  
        b_response = bytes(response, 'utf-8')
        conexao.sendall(b_response)
