import socket

from argparse import ArgumentParser
from parse import parse
from primes import *
from random import randint
from time import perf_counter_ns


def check_inputs(cod, n):
  return cod > 1000000 and len(primes(cod)) >= 2 * n


argparser = ArgumentParser()
argparser.add_argument("hostname", type=str)
argparser.add_argument("portnumber", type=int)
args = argparser.parse_args()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('localhost', randint(49152, 65535)))
  print(s)

  # Communication with server 2
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as c:
    c.connect((args.hostname, args.portnumber))
    print(c)

    s.listen()
    while True:
      conexao, addr = s.accept()
      with conexao:
        #print("client connected: ", addr)
        while True:
          dados = conexao.recv(1024)
          if not dados:
            break

          msg = dados.decode()
          # handle null-terminated strings
          msg = msg.replace("\x00", "")
  
          parsed = parse("{},{}", msg)
          if parsed is None:
            break
  
          cod = int(parsed[0])
          n = int(parsed[1])
  
          start = perf_counter_ns()
          
          ok = check_inputs(cod, n)
          
          end = perf_counter_ns()
          # ms from ns
          t = (end - start) / 1e6
          print("check: {:.2f}ms".format(t), end=" ")
  
          b_response = b'invalid input'

          if ok:
            msg = "{},{}".format(cod, n)
            b_string = bytes(msg, 'utf-8')
            c.sendall(b_string)
            dados = c.recv(1024)
            
            response = dados.decode()
            print(response, end=" | ")
            b_response = bytes(response, 'utf-8')
          
          conexao.sendall(b_response)

