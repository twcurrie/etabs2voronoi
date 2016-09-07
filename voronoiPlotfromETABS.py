import csv 
import os
from scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import numpy as np

class Joint:
	"""Joint class for vertices"""

	def __init__(self, uniqueID, xCoord, yCoord, zCoord):
		self.x = xCoord*12 # ETABS provides in ft by default
		self.y = yCoord*12
		self.z = zCoord*12
		self.id = uniqueID

class Joints:
	"""Array of joints"""
	def __init__(self):
		self.inventory = {}
	
	def addJoint(self, joint):
		self.inventory[joint.id] = joint

class Column:
	"""Column class"""

	def __init__(self, label, uniqueName, startPoint, endPoint):
		self.label = label
		self.uniqueName = uniqueName
		self.startJoint = startPoint
		self.endJoint = endPoint
	
class Columns:
	"""Dictionary of columns"""
	def __init__(self):
		self.inventory = {}

	def addColumn(self, column):
		self.inventory[column.uniqueName] = column

def importJoints():
	"""Imports joints into dictionary of objects"""
	
	modelJoints = Joints()

	with open('jointLocations.csv','rb') as csvfile:
		csvRead = csv.reader(csvfile, delimiter=",")
		for row in csvRead:
			joint = Joint(int(row[2]),float(row[3]),
					float(row[4]),float(row[5]))
			modelJoints.addJoint(joint)
	
	return modelJoints

def importColumns(modelJoints):
	"""Imports columns into dictionary of objects"""
	modelColumns = Columns()

	with open('columnConnectivity.csv','rb') as csvfile:
		csvRead = csv.reader(csvfile, delimiter=",")
		for row in csvRead:
			joints = row[3].split(";")
			startJoint = modelJoints.inventory[int(joints[0])]
			endJoint = modelJoints.inventory[int(joints[1])]
			newColumn = Column(row[1],int(row[2]),
					startJoint, endJoint)
			modelColumns.addColumn(newColumn)
	return modelColumns

def getColumnsEndingAt(columns, zLevel):
	"""Returns columns w/ endPoint at zLevel"""
	columnGroup = {}

	for columnID, column in columns.inventory.iteritems():
		diff = abs(zLevel - column.endJoint.z)
		if diff <= 0.001:
			columnGroup[column.uniqueName] = column
	return columnGroup

def voronoiPlot(columns,level):
	"""Creates voronoi plot using scipy library"""
	levelColumns = getColumnsEndingAt(columns,level)

	pointsAtLevel = []
	for columnID, column in levelColumns.iteritems():
		pointsAtLevel.append([column.endJoint.x,column.endJoint.y])

	inputPoints = np.array(pointsAtLevel)
	vor = Voronoi(inputPoints)

	voronoi_plot_2d(vor)
	plt.show()
	return


if __name__ == "__main__":
	joints = importJoints()
	columns = importColumns(joints)
	
	levelTwo = 16*12 # level two elevation
	levelThree = 28.75*12 # level three elevation

	voronoiPlot(columns,levelTwo)

		
