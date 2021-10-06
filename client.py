import socket
import pandas as pd

from time import perf_counter_ns

df = pd.read_csv('file.csv', header=None, names=['Cod', 'n'])

#initial_code = int(input("Codigo Inicial: "))
#n = int(input("n: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect(("127.0.0.1", 50022))
  print(s)
  j = 1
  sum_t = 0

  for i in range(len(df)):
    start = perf_counter_ns()  

    initial_code = df.loc[i, 'Cod']
    n = df.loc[i, 'n']
    msg = f"{initial_code}, {n}"
    b_string = bytes(msg, 'utf-8')
    s.sendall(b_string)
    dados = s.recv(1024)
    print(f"Resposta do servidor: {dados.decode()}")
    finish = perf_counter_ns()
  
    t = (finish - start) / 1000000
    sum_t += t

    print("{:.2f}ms".format(t))

    if j < 10: 
      j += 1
    else:
      break;

  avg_t = sum_t / 10

  print("avg: {:.2f}ms".format(avg_t))

#    if finish-start > 5000000000:
#      break
