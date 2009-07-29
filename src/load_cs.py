# load_cs.py
# script to run from blender, allowing to visualise a agents CS

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
	ob.setLocation(normalize(dims, coors, global_dim))
	ob.setSize(0.2, 0.2, 0.2)
	ob.link(passedMesh)
	passedScene.link(ob)
	return ob


def createObject(dims, coors):
	"""creates an object for given dimensions and places this in the scene
	"""
	localScene = Scene.GetCurrent() #Create a single sphere.
	sphere = Mesh.Primitives.UVsphere()
	mat1 = Blender.Material.New('Mat1') # create material
	mat1.rgbCol = normalize(dims, coors) # set colour
	sphere.materials = [mat1]
	tempSphere = makeSphere("sphere", sphere, localScene, dims, coors)
	Redraw(-1)
	

def parseCS(file_name):
	""" reads a conceptual space from an agent out an given xml file
		returns a etree object of the CS
	"""
	fileHandle = open (file_name) 			# read file
	tree = etree.parse(fileHandle)			# parse to ElementTree object
	fileHandle.close()						# close file
	root = tree.getroot()					# get root as Element object

	#print(etree.tostring(tree))

	listing = root.getchildren()
	return listing
	

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




def loadAgentCS(agent_filename):
	"""loads the agent CS into Blender
	"""
	agent_cs = parseCS(agent_filename)
	concepts = []
	for i in agent_cs:
		# collect concepts
		if i.tag == "concept":
			for j in i:
				if j.tag == "domains":
					domains = []
					for k in j:
						if k.values() == ["rgb"]:
							coors = []
							for l in k:
								for m in l:
									if m.tag == "value":
										coors.append(float(m.text))
						domains.append(["rgb", coors])
			concepts.append(domains)
	
	# create Blender objects from concepts
	for i in concepts:
		for j in i:
			if j[0] == "rgb":
				createObject(rgb_dim, j[1])


loadAgentCS("CP_learner.xml")


#for i in test_coors:
#	createObject(rgb_dim, i)
	