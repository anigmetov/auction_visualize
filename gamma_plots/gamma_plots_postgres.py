#!/usr/bin/env python3

import math
import sys
import psycopg2
# import time
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt


conn = psycopg2.connect("dbname = 'db_tests' user = 'narn' password = ''")
cur = conn.cursor()

print("connected to DB")
cur.execute("""select num_phase,
                      num_rounds,
                      num_unassigned_bidders,
                      gamma,
                      partial_cost,
                      epsilon,
                      num_unassigned_normal_bidders,
                      num_unassigned_diag_bidders,
                      num_unassigned_normal_items,
                      num_unassigned_diag_items,
                      num_normal_assignments,
                      num_diag_assignments,
                      num_duplicates_top_heap,
                      relative_error
            from narn.morozov_test_result_plots
            where points_number = 10000
            order by num_phase, num_rounds""")

rows = cur.fetchall()

print("fetched rows")

# choose_phase = lambda x: x.num_phase == 9
def choose_phase(x):
    return True
    # return x.num_phase >= 4

x_vals = [r[1] for r in rows if choose_phase(r)]
# y_gamma = [ math.log(r[3] + 1.0) for r in rows if choose_phase(r)]
y_unassigned = [r[2] for r in rows if choose_phase(r)]
# y_partial_cost = [ r[4] for r in rows if choose_phase(r)]
y_unassigned_diag_bidders =  [ r[7] for r in rows if choose_phase(r)]
y_heap_duplicates =  [ r[12] for r in rows if choose_phase(r)]
# y_unassigned_normal_bidders =  [ r[6] for r in rows if choose_phase(r)]
y_relative_error =  [ min(r[13], 2.0) for r in rows if choose_phase(r)]
y_true_relative_error =  [ min(2.0, abs(r[4] - 636.24) / 636.24) for r in rows if choose_phase(r)]


fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
# ax3  = ax2.twinx()


l_unassigned_diag, = ax1.plot(x_vals, y_unassigned_diag_bidders, 'r', label ="Unassigned diagonal bidders")
# ax1.plot(x_vals, y_unassigned_normal_bidders, 'g')

# ax1.plot(x_vals, y_relative_error, 'r')
l_heap_duplicates, = ax2.plot(x_vals, y_heap_duplicates, 'g', label = "Heap top size")

plt.legend(handles = [l_unassigned_diag, l_heap_duplicates], labels = ["Unassigned diagonal bidders", "Heap top size"])

# ax2.plot(x_vals, y_gamma, 'r')
# ax2.set_ylabel("Gamma")
#
# ax3.plot(x_vals, y_partial_cost, 'g')
# ax3.set_ylabel("Partial cost")

plot_file_name = "plot_10000_duplicates.png"

plt.savefig(plot_file_name, dpi = 1200)

plt.clf()
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

line_unassigned, = ax1.plot(x_vals, y_unassigned, 'k', label = "Unassigned bidders")
ax1.set_xlabel("Round")
ax1.set_ylabel("# Unassigned")

line_rel_error, = ax2.plot(x_vals, y_relative_error, 'r', label = "Relative error")
ax2.set_ylabel("Relative error")

plt.legend(handles = [line_unassigned, line_rel_error], labels = ["Unassigned bidders", "Relative error"])

plot_file_name = "plot_10000_unassigned_relative_error.png"
plt.savefig(plot_file_name, dpi = 1200)
