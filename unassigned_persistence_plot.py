#!/usr/bin/env python3



import math
import time
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os.path
import pickle

class PlotLogRow:

    def __init__(self, line):
        s = line.split(" ")
        self.num_phase = int(s[0])
        self.num_round = int(s[1])
        self.n_unassigned = int(s[2])
        self.unassigned_items_persistence = float(s[3])
        self.unassigned_bidders_persistence = float(s[4])
        self.partial_cost = float(s[6])
        self.total_bidders_persistence = float(s[7])
        self.total_items_persistence = float(s[8])



rows = []
rows_pickled_fname = "large_plot_rows"

if os.path.exists(rows_pickled_fname):
    rows = pickle.load(open(rows_pickled_fname, "rb"))
    print("read pickled")
else:
    with open("plot_logger_large.txt") as f:
        # rows = [ PlotLogRow(s) for s in f if (s.startswith("8 ") or s.startswith("7 ") or s.startswith("6 ") or s.startswith("1 "))]
        rows = [ PlotLogRow(s) for s in f if (s.startswith("8 ") or s.startswith("7 "))]
        print("read file ok")

        pickle.dump(rows, open(rows_pickled_fname, "wb"))
        print("pickled rows ok")

        f.close()

choose_phase = lambda x: x.num_phase == 8

x_vals = [r.num_round for r in rows if choose_phase(r)]
y_items = [(r.unassigned_items_persistence) for r in rows if choose_phase(r)]
y_bidders = [r.unassigned_bidders_persistence for r in rows if choose_phase(r)]
y_unassigned = [(r.n_unassigned + 1) for r in rows if choose_phase(r)]
y_partial_cost = [r.partial_cost for r in rows if choose_phase(r)]
plt.plot(x_vals, y_items, 'r')
# plt.plot(x_vals, y_bidders, 'k')
plt.plot(x_vals, y_unassigned, 'g')
plt.plot(x_vals, y_partial_cost, 'c')
plt.savefig("plot_large_80000.png")
