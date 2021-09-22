"""import sympy
import concurrent.futures


def tCalculaPrimo(data):
    #primos = []
    primos = 0
    for i in range(len(data)):
        if sympy.isprime(data[i]):
            #primos.append(data[i])
            primos += 1
    return primos"""

import sympy
import socket

def evaluation(cod, n):
    i = 0
    ant = cod
    while(i < n):
        ant -= 1
        if sympy.isprime(ant):
            i += 1
    i = 0
    pos = cod
    while(i < n):
        pos += 1
        if sympy.isprime(ant):
            i += 1

    result = pos*ant
    return result


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('127.0.0.1', 50003))
  print(s)
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