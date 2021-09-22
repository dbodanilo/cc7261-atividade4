import socket
initial_code = int(input("Codigo Inicial: "))
n = int(input("n: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect(("127.0.0.1", 50002))
  print(s)
  msg = f"{initial_code}, {n}"
  b_string = bytes(msg, 'utf-8')
  s.sendall(b_string)
  dados = s.recv(1024)
  print(f"Resposta do servidor: {dados.decode()}")