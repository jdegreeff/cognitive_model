# load_cs.py
# script to run from blender, allowing to visualise an agents CS

from __future__ import division
from lxml import etree
import Blender
from Blender import *


test_coors = [[255.0, 0.0, 0.0],[0.0, 255.0, 0.0],[0.0, 0.0, 255.0]]

rgb_dim = [0.0, 255.0]
global_dim = [0.0, 10.0]


def normalize(space, coordinates, glob=None):
	""" normalize dimensions for a given space
		space = [min,max], coordinates = [x, x, ....,x]
		glob determines the global dimensions of the visual environment
	"""
	dim_new = []
	for i in coordinates:
		if glob:
			dim_new.append(i/space[1]*glob[1])
		else:
			dim_new.append(i/space[1])
	return dim_new


def makeSphere(name, passedMesh, passedScene, dims, coors):
	ob = Object.New("Mesh",name)
	ob.setLocation(normalize(dims, [coors[0][0],coors[1][0],coors[2][0]], global_dim))
	size = [coors[0][1],coors[1][1],coors[2][1]]
	new_size = []
	for i in size:
		if i > 3.0:
			new_size.append(normalize(dims, [i], global_dim)[0])
		else:
			new_size.append(0.1)
	ob.setSize(new_size)
	ob.link(passedMesh)
	passedScene.link(ob)
	return ob


def createObject(dims, coors):
	"""creates an object for given dimensions and places this in the scene
	"""
	localScene = Scene.GetCurrent()       
	sphere = Mesh.Primitives.UVsphere()     #Create a single sphere.
	mat1 = Blender.Material.New('Mat1')    # create material
	mat1.rgbCol = normalize(dims, [coors[0][0],coors[1][0],coors[2][0]])   # set colour
	mat1.setAlpha(0.8)
	sphere.materials = [mat1]
	makeSphere("sphere", sphere, localScene, dims, coors)
	Redraw(-1)
	

def parseCS(file_name):
	""" reads a conceptual space from an agent out an given xml file
		returns a etree object of the CS
	"""
	fileHandle = open (file_name) 			# read file
	tree = etree.parse(fileHandle)			# parse to ElementTree object
	fileHandle.close()						# close file
	root = tree.getroot()					# get root as Element object
	return root.getchildren()               # returns the content of root
	

def printAgentCS(agent_filename):
	"""prints the agent CS to console
	"""
	agent_cs = parseCS(agent_filename)
	for i in agent_cs:
	    if i.tag == "agent":
	        print i.text
	    elif i.tag == "concept":
	        print "concept: " + str(i.items())
	        for j in i:
	            if j.tag == "domains":
	                for l in j:
	                    print "domain: " + str(l.items())
	                    for k in l:
	                        print "	" + k.tag, k.values()
	                        for n in k:
	                            print "	" + n.tag + ": " + n.text
	            else:
	                for m in j:
	                    print m.tag + ": " + m.text


def setText(text_string, coors):
	"""sets a given text in the current environment on the given coordinates
	"""
	localScene = Scene.GetCurrent()  
	txt = Text3d.New() 
	txt.setText(text_string)
	txt.setSize(0.3)
	msg = localScene.objects.new(txt) 
	msg.setLocation(normalize(rgb_dim, coors, global_dim))
	msg.rot = [1.57, 0.0, 0.0]     # set rotation
	mat = Material.New('newMat')    # create a new Material called 'newMat' 
	mat.rgbCol = normalize(rgb_dim, coors, global_dim)    # change its colour 
	msg.setMaterials([mat])
	Window.RedrawAll() 



def loadAgentCS(agent_filename):
	"""loads the agent CS into Blender
	"""
	agent_cs = parseCS(agent_filename)
	concepts = []
	for i in agent_cs:
		# collect concepts
		if i.tag == "concept":
			concept_label = i.values()
			for j in i:
				if j.tag == "domains":
					domains = []
					for k in j:
						if k.values() == ["rgb"]:
							coors = []
							for l in k:
								dim = []
								for m in l:
									dim.append(float(m.text))
								coors.append(dim)
						domains.append(["rgb", coors])
			concepts.append([concept_label[1], domains])
	
	# create Blender objects from concepts
	for i in concepts:
		concept_label = i[0]
		for j in i[1]:
			if j[0] == "rgb":
				createObject(rgb_dim, j[1])
				text_location = [j[1][0][0] + 6.0, j[1][1][0] - j[1][1][1], j[1][2][0] + j[1][2][1]]
				setText(concept_label, text_location)
				

loadAgentCS("CP_learner.xml")
