
import sympy
import socket
import concurrent.futures



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


def eval_backward(cod, n):
  i = 0
  ant = cod
  while(i < n):
    ant -= 1
    if sympy.isprime(ant):
      i += 1
  return ant

def eval_forward(cod, n):
  i = 0
  pos = cod
  while(i < n):
    pos += 1
    if sympy.isprime(pos):
      i += 1
  return pos

def evaluation(cod, n):
  with concurrent.futures.ThreadPoolExecutor() as executor:
    future_ant = executor.submit(eval_backward, cod, n)
    future_pos = executor.submit(eval_forward, cod, n)

    return future_ant.result()*future_pos.result()       


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('127.0.0.1', 50003))
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