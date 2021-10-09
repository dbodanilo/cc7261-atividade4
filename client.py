import socket

from argparse import ArgumentParser
from pandas import read_csv
from parse import parse
from sys import stdin
from time import perf_counter_ns


argparser = ArgumentParser()
argparser.add_argument("hostname", type=str)
argparser.add_argument("portnumber", type=int)
argparser.add_argument("max_runs", type=int)
args = argparser.parse_args()


# test runs
max_runs = 5 if args.max_runs is None else args.max_runs
# for each run (ms)
time_limit = 5000

# for each run 
run_c = 0  
run_t = 0

# across all runs
all_c = 0
all_t = 0

# number of runs
nruns = 0


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  # client -> server
  s.connect((args.hostname, args.portnumber))
  print(s)

  for line in stdin:
    result = parse("{},{}", line)

    if result is None: 
      break;

    initial_code = int(result[0])
    n = int(result[1])

    msg = "{},{}".format(initial_code, n)
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
    print("{:.2f}ms".format(t), end=" ")
    run_t += t
    all_t += t
  
    nruns = int(all_t / time_limit)

    print(dados.decode(), end=" | ")

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
  nruns = max(nruns, 1)
  avg_c = all_c * time_limit / max(all_t, time_limit)
  
  print("\n---")
  print("ran for {} seconds {} times".format(secs, nruns))
  print("average of {:.0f} codes each run".format(avg_c)) 
  print("---\n")

