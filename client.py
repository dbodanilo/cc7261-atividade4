import socket
import pandas as pd

from time import perf_counter_ns

df = pd.read_csv('file.csv', header=None, names=['Cod', 'n'])

#initial_code = int(input("Codigo Inicial: "))
#n = int(input("n: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect(("127.0.0.1", 50002))
  print(s)
  start = perf_counter_ns()  
  for i in range(len(df)):
    initial_code = df.loc[i, 'Cod']
    n = df.loc[i, 'n']
    msg = f"{initial_code}, {n}"
    b_string = bytes(msg, 'utf-8')
    s.sendall(b_string)
    dados = s.recv(1024)
    print(f"Resposta do servidor: {dados.decode()}")
    finish = perf_counter_ns()

    if finish-start > 5000000000:
      break