import socket
import pandas as pd

from time import perf_counter_ns

datafile = "file.csv"
#datafile = input()

max_runs = 50

df = pd.read_csv(datafile, header=None, names=['Cod', 'n'])

#initial_code = int(input("Codigo Inicial: "))
#n = int(input("n: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect(("127.0.0.1", 50022))
  print(s)
  j = 1
  sum_t = 0

  # every 5 seconds
  ncodes = 0
  
  # across all tests
  sum_c = 0

  # number of 5-second runs
  nruns = 1

  for i in range(len(df)):
    start = perf_counter_ns()  

    initial_code = df.loc[i, 'Cod']
    n = df.loc[i, 'n']

    msg = f"{initial_code}, {n}"   
    print(msg, end=": ")

    b_string = bytes(msg, 'utf-8')
    s.sendall(b_string)

    dados = s.recv(1024)
    print(f"{dados.decode()}", end=" | ")
    ncodes += 1

    finish = perf_counter_ns()
  
    t = (finish - start) / 1000000
    sum_t += t

    #print("{:.2f}ms".format(t))

    if sum_t > 5000:
      print("\n---")
      print(f"generated {ncodes} codes") 

      avg_t = sum_t / ncodes
      print("average {:.2f}ms per code".format(avg_t))
      print("---\n\n")

      sum_c += ncodes
      nruns += 1
      if nruns >= max_runs:
        break

      ncodes = 0
      sum_t = 0


  print("\n---")
  print(f"ran {nruns} times")
  print(f"average of {sum_c/nruns:.0f} codes per 5 seconds") 
  print("---\n")

