# io.py
# input/output file

from __future__ import division
import csv
import numpy
from lxml import etree
from copy import deepcopy


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
        
        
def save_matrix(agent_name, lexicon):
    """ saves the association matrix of an agent to a file
    """
    filename = "matrix_" + agent_name + ".csv"
    out_file = csv.writer(open(filename, 'w'), delimiter=',', quotechar='|')
    tags = deepcopy(lexicon.tags)
    tags.insert(0,"")
    out_file.writerow(tags)
    for count, i in enumerate(lexicon.matrix):
        output = numpy.hstack((lexicon.labels[count], i))
        out_file.writerow(output)
    

def save_cp_to_xml(agent_name, cp, lex):
    """ saves the given cp and lexicon to an xml file
    """
    #concept format: [ "tag", [ [ "d1", value, sd], [ "d2", value, sd], [ "d3", value, sd] ], [concept_use, concept_success] ]
    filename = "CP_" + agent_name + ".xml"
    root = etree.Element("root")
    etree.SubElement(root, "agent").text = agent_name
    for i in cp.concepts:
        concept = etree.SubElement(root, "concept", label = lex.get_label(i.tag), tag = str(i.tag))
        domains = etree.SubElement(concept, "domains")
        for j in i.domains:
            domain = etree.SubElement(domains, "domain", name = str(j.name))
            for l in j.dimensions:
                dimension = etree.SubElement(domain, "dimension", dimension = str(l[0])) 
                etree.SubElement(dimension, "value").text = str(l[1])
                etree.SubElement(dimension, "sd").text = str(l[2])
        usage = etree.SubElement(concept, "usage")
        etree.SubElement(usage, "use").text = str(i.concept_use)
        etree.SubElement(usage, "success").text = str(i.concept_success)
    out = open(filename,'w')
    out.write(etree.tostring(root))
    
    
    
   
#etree.SubElement(root, "child").text = "Child 1"
#etree.SubElement(root, "child").text = "Child 2"
#another = etree.SubElement(root, "another")
#
#etree.SubElement(another, "test").text = "test 3"
#
#print(etree.tostring(root, pretty_print=True))
#
#out = open('output.xml','w')
#out.write ( etree.tostring(root) )

