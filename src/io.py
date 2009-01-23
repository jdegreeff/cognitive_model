# io.py
# input/output file

from __future__ import division
import csv


def open_datafile(mode, space):
    filename = mode + space + ".txt"
    openfile = csv.reader(open(filename), delimiter='\t')
    list = []
    for row in openfile:
        colour = [float(row[0]), float(row[1]), float(row[2])]
        list.append(colour)
    return list
