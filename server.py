import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.bind(('127.0.0.1', 50002))
  print(s)
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
          c.connect(("127.0.0.1", 50003))
          print(c)
          msg = f"{cod}, {n}"
          b_string = bytes(msg, 'utf-8')
          c.sendall(b_string)
          dados = c.recv(1024)
          print(f"Resposta do servidor: {dados.decode()}")
          
          response = str(dados.decode())
          b_response = bytes(response, 'utf-8')
          conexao.sendall(b_response)