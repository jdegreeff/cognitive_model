# io 0.8.6
# input/output file

from __future__ import division
import csv
from lxml import etree


def open_datafile(mode, domain):
    filename = mode + domain + ".txt"
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
    
    

def save_cp_to_xml(agent_name, cp, lex):
    """ saves the given cp and lexicon to an xml file
    """
    #concept format: [ "tag", [ [ "d1", value, sd], [ "d2", value, sd], [ "d3", value, sd] ], [concept_use, concept_success] ]
    filename = "CP_" + agent_name + ".xml"
    root = etree.Element("root")
    etree.SubElement(root, "agent").text = agent_name
    for i in cp.concepts:
        concept = etree.SubElement(root, "concept")
        etree.SubElement(concept, "label").text = lex.get_label(i[0])
        etree.SubElement(concept, "tag").text = str(i[0])
        coors = etree.SubElement(concept, "coors")
        for j in i[1]:
            value = etree.SubElement(coors, "dimension")
            etree.SubElement(value, "name").text = str(j[0])
            etree.SubElement(value, "value").text = str(j[1])
            etree.SubElement(value, "sd").text = str(j[2])
        if len(i) > 2:
            usage = etree.SubElement(concept, "usage")
            etree.SubElement(usage, "use").text = str(i[2][0])
            etree.SubElement(usage, "success").text = str(i[2][1])
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

