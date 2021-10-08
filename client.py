import socket

from pandas import read_csv
from time import perf_counter_ns

datafile = "file.csv"
#datafile = input()

# test runs
max_runs = 5
# for each run (ms)
time_limit = 5000

df = read_csv(datafile, header=None, names=['Cod', 'n'])

#initial_code = int(input("Codigo Inicial: "))
#n = int(input("n: "))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect(("127.0.0.1", 50022))
  print(s)

  # for each run 
  run_c = 0  
  run_t = 0

  # across all runs
  all_c = 0
  all_t = 0

  # number of runs
  nruns = 0

  for i in range(len(df)):
    initial_code = df.loc[i, 'Cod']
    n = df.loc[i, 'n']

    msg = "{}, {}".format(initial_code, n)   
    print(msg, end=": ")

    b_string = bytes(msg, 'utf-8')

    start = perf_counter_ns()

    s.sendall(b_string)
    dados = s.recv(1024)
    run_c += 1
    all_c += 1

    finish = perf_counter_ns()
    # ms from ns
    t = (finish - start) / 1e6
    #print("{:.2f}ms".format(t))
    run_t += t
    all_t += t
  
    nruns = int(all_t / time_limit)

    print("{}".format(dados.decode()), end=" | ")

    if run_t > time_limit:
      print("\n---")
      print("generated {} codes".format(run_c)) 

      avg_t = run_t / run_c
      print("average {:.2f}ms per code".format(avg_t))
      print("---\n")

      run_c = 0
      run_t = 0

      if nruns >= max_runs:
        break

  # s from ms
  secs = int(time_limit/1e3)

  # avoid division by zero
  nruns = max(1, nruns)
  avg_c = all_c * time_limit / all_t

  print("\n---")
  print("ran for {} seconds {} times".format(secs, nruns))
  print("average of {:.0f} codes each run".format(avg_c)) 
  print("---\n")

