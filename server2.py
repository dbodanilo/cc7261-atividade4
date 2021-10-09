import socket

from concurrent.futures import ThreadPoolExecutor
from parse import parse
from primes import check_backward, check_forward, primes
from random import randint
from time import perf_counter_ns


def evaluation(cod, n):
  primes_cod = primes(cod)
  nprimes_cod = len(primes_cod)

  with ThreadPoolExecutor() as executor:
    future_ant = executor.submit(check_backward, primes_cod, n)
    future_pos = executor.submit(check_forward, nprimes_cod, n)

    left = future_ant.result()
    #print(f"left: {left}")

    right = future_pos.result()
    #print(f"right: {right}")
 
    code = left * right

    return code


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('localhost', randint(49152, 65535)))
  print(s)

  s.listen()
  while True:
    conexao, addr = s.accept()
    with conexao:
      #print("server connected: ", addr)
      while True:
        dados = conexao.recv(1024)
        if not dados:
          break

        msg = dados.decode()
        # handle null-terminated strings
        msg = msg.replace("\x00", "")
  
        result = parse("{:d},{:d}", msg) 
        if result is None:
          break

        cod, n = result

        # evaluation
        start = perf_counter_ns()

        key = evaluation(cod, n)

        end = perf_counter_ns()
        # ms from ns
        t = (end - start) / 1e6
        print("eval: {:.2f}ms".format(t), end=" ")
        
        response = str(key)  
        print("code: ", response, end=" | ")
        b_response = bytes(response, 'utf-8')
        conexao.sendall(b_response)

