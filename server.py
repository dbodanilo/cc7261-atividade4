import socket
import sympy
from primes import check_inputs


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(('localhost', 50022))
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
            c.connect(("127.0.0.1", 50023))
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
