#!/usr/bin/env python3


import math
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import numpy as np
import ast



class LogRow:

    def __init__(self, line):
        # expected format: round # current_bidder # current_item # unassigned_bidders # unassigned_items # epsilon
        # points are written as (x, y)
        # unassigned_bidders/items are in Python format [(x_1, y_1), ..., (x_n, y_n)]
        # so we can parse them with literal evaluation (slow, but simple)
        ss = [s.strip() for s in line.split("#")]

        self.round = int(ss[0])

        bidder = ast.literal_eval(ss[1])
        self.bidder_x = bidder[0]
        self.bidder_y = bidder[1]

        item = ast.literal_eval(ss[2])
        self.item_x = item[0]
        self.item_y = item[1]

        unassigned_bidders = ast.literal_eval(ss[3])
        self.unassigned_bidders_x = [ub[0] for ub in unassigned_bidders]
        self.unassigned_bidders_y = [ub[1] for ub in unassigned_bidders]

        unassigned_items = ast.literal_eval(ss[4])
        self.unassigned_items_x = [ui[0] for ui in unassigned_items]
        self.unassigned_items_y = [ui[1] for ui in unassigned_items]

        self.n_unassigned = len(self.unassigned_bidders_x)

        self.epsilon = ast.literal_eval(ss[5])

        if (self.n_unassigned > 0):
            self.min_x = min(self.bidder_x,
                             self.item_x,
                             min(self.unassigned_bidders_x),
                             min(self.unassigned_items_x))

            self.min_y = min(self.bidder_y,
                             self.item_y,
                             min(self.unassigned_bidders_y),
                             min(self.unassigned_items_y))

            self.max_x = max(self.bidder_x,
                             self.item_x,
                             max(self.unassigned_bidders_x),
                             max(self.unassigned_items_x))

            self.max_y = max(self.bidder_y,
                             self.item_y,
                             max(self.unassigned_bidders_y),
                             max(self.unassigned_items_y))
        else:
            self.min_x = min(self.bidder_x, self.item_x)
            self.min_y = min(self.bidder_y, self.item_y)
            self.max_x = max(self.bidder_x, self.item_x)
            self.max_y = max(self.bidder_y, self.item_y)


class AuctionVis:

    def __init__(self):
        pass

    def read_file(self, fname):
        with open(fname) as f:
            self.rows = [LogRow(line) for line in f]

        self.min_x = min([r.min_x for r in self.rows])
        self.min_y = min([r.min_y for r in self.rows])
        self.max_x = min([r.max_x for r in self.rows])
        self.max_y = min([r.max_y for r in self.rows])


    def plot_process(self, n_unassigned):
        #idx = self.n_unassigned_array.index(n_unassigned)
        fig, ax = plt.subplots()
        ax.set_xlim(self.min_x - 2.0, self.max_x + 2.0)
        ax.set_ylim(self.min_y - 2.0, self.max_y + 4.0)

        idx = 0

        r = self.rows[idx]

        bidder_point, = ax.plot([r.bidder_x],[r.bidder_y], 'ro')
        item_point, = ax.plot([r.item_x], [r.item_y], 'co')

        unassigned_bidders, = ax.plot(r.unassigned_bidders_x, r.unassigned_bidders_y, 'ko', linestyle = "None")
        unassigned_items, = ax.plot(r.unassigned_items_x, r.unassigned_items_y, 'gx', linestyle = "None")

        edge_line, = ax.plot([r.bidder_x,r.item_x], [r.bidder_y, r.bidder_y], color = 'blue', linewidth = 1)

        unassigned_text = ax.text(0.5, 1, repr(r.n_unassigned),
                                  horizontalalignment = 'center',
                                  verticalalignment = 'top',
                                  transform = ax.transAxes)

        idx += 1

        for r in self.rows[idx:]:
            bidder_point.set_data(r.bidder_x, r.bidder_y)
            item_point.set_data(r.item_x, r.item_y)
            edge_line.set_data([r.bidder_x, r.item_x], [r.bidder_y, r.item_y])
            unassigned_bidders.set_data(r.unassigned_bidders_x, r.unassigned_bidders_y)
            unassigned_items.set_data(r.unassigned_items_x, r.unassigned_items_y)
            unassigned_text.set_text(repr(r.n_unassigned))
            plt.pause(2)

    def write_to_files(self, fname_format, n_unassigned):
        #idx = self.n_unassigned_array.index(n_unassigned)
        fig, ax = plt.subplots()
        ax.set_xlim(self.min_x - 2.0, self.max_x + 2.0)
        ax.set_ylim(self.min_y - 2.0, self.max_y + 4.0)

        idx = 0
        img_num = 0

        r = self.rows[idx]

        bidder_point, = ax.plot([r.bidder_x],[r.bidder_y], 'ro')
        item_point, = ax.plot([r.item_x], [r.item_y], 'co')

        unassigned_bidders, = ax.plot(r.unassigned_bidders_x, r.unassigned_bidders_y, 'ko', linestyle = "None")
        unassigned_items, = ax.plot(r.unassigned_items_x, r.unassigned_items_y, 'gx', linestyle = "None")

        edge_line, = ax.plot([r.bidder_x,r.item_x], [r.bidder_y, r.bidder_y], color = 'blue', linewidth = 1)

        unassigned_text = ax.text(0.5, 1, repr(r.n_unassigned),
                                  horizontalalignment = 'center',
                                  verticalalignment = 'top',
                                  transform = ax.transAxes)

        img_name = fname_format.format(img_num)
        plt.savefig(img_name)
        img_num += 1

        idx += 1

        for r in self.rows[idx:]:
            bidder_point.set_data(r.bidder_x, r.bidder_y)
            item_point.set_data(r.item_x, r.item_y)
            edge_line.set_data([r.bidder_x, r.item_x], [r.bidder_y, r.item_y])
            unassigned_bidders.set_data(r.unassigned_bidders_x, r.unassigned_bidders_y)
            unassigned_items.set_data(r.unassigned_items_x, r.unassigned_items_y)
            unassigned_text.set_text(repr(r.n_unassigned))

            img_name = fname_format.format(img_num)
            plt.savefig(img_name)
            img_num += 1



    # don't use, too slow
    def write_to_video(self, filename):
        FFMpegWriter = manimation.writers['ffmpeg']
        metadata = dict(title='Visualize Auction', artist='Matplotlib', comment='')
        writer = FFMpegWriter(fps=24, metadata=metadata)

        #idx = self.n_unassigned_array.index(n_unassigned)
        fig, ax = plt.subplots()
        ax.set_xlim(self.min_x - 2.0, self.max_x + 2.0)
        ax.set_ylim(self.min_y - 2.0, self.max_y + 2.0)

        idx = 0

        r = self.rows[idx]

        with writer.saving(fig, filename, 600):

            bidder_point, = ax.plot([r.bidder_x],[r.bidder_y], 'ro')
            item_point, = ax.plot([r.item_x], [r.item_y], 'co')

            unassigned_bidders, = ax.plot(r.unassigned_bidders_x, r.unassigned_bidders_y, 'ko', linestyle = "None")
            unassigned_items, = ax.plot(r.unassigned_items_x, r.unassigned_items_y, 'gx', linestyle = "None")

            edge_line, = ax.plot([r.bidder_x,r.item_x], [r.bidder_y, r.bidder_y], color = 'blue', linewidth = 1)
            writer.grab_frame()
            unassigned_text = ax.text(0.5, 1, repr(r.n_unassigned),
                                      horizontalalignment = 'center',
                                      verticalalignment = 'top',
                                      transform = ax.transAxes)

            idx += 1

            j = 0

            for r in self.rows[idx:]:
                bidder_point.set_data(r.bidder_x, r.bidder_y)
                item_point.set_data(r.item_x, r.item_y)
                edge_line.set_data([r.bidder_x, r.item_x], [r.bidder_y, r.item_y])
                unassigned_bidders.set_data(r.unassigned_bidders_x, r.unassigned_bidders_y)
                unassigned_items.set_data(r.unassigned_items_x, r.unassigned_items_y)
                unassigned_text.set_text(repr(r.n_unassigned))
                writer.grab_frame()
                j +=1
                if (j % 1000 == 0):
                    print('Row {0} processed'.format(j))



if __name__ == "__main__":
    av = AuctionVis()
    # av.read_file("ll.txt")
    av.read_file("wasserstein_log1.txt")
    # av.plot_process(4)
    # av.write_to_file("tee.mp4")

    fname_format = "image-{:08}.png"
    av.write_to_files(fname_format, 9)

