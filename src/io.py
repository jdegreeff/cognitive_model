# io.py
# input/output file

from __future__ import division
import csv
from lxml import etree


def open_datafile(mode, space):
    filename = mode + space + ".txt"
    openfile = csv.reader(open(filename), delimiter='\t')
    list = []
    for row in openfile:
        colour = [float(row[0]), float(row[1]), float(row[2])]
        list.append(colour)
    return list


def write_output(name, output):
    """ write output file
        output = [ [value1, value2, value n], ...[value1, value2, value n] ]
    """
    filename = "out" + name + ".csv"
    out_file = csv.writer(open(filename, 'w'), delimiter=',', quotechar='|')
    for i in output:
        out_file.writerow(i)
        
        
def write_output2(name, output):
    """ write output file
        output = [ [value1, value2, value n], ...[value1, value2, value n] ]
    """
    filename = "out" + name + ".csv"
    out_file = csv.writer(open(filename, 'w'), delimiter=',', quotechar='|')
    for i in output:
        out_file.writerow(i[2])



def drop_cp(agent_name, cp):
    """ saves the CP of an agent to a file
    """
    filename = "CP_" + agent_name + ".csv"
    out_file = csv.writer(open(filename, 'w'), delimiter=',', quotechar='|')
    for i in cp.concepts:
        out_file.writerow(i)
    