# -*- coding: UTF-8 -*-
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
from math import log
import operator
import pickle

"""
Calculate the Shannon entropy for a given data set
Parameters:
	dataSet 
Returns:
	shannonEnt 
"""
def calcShannonEnt(dataSet):
	numEntires = len(dataSet)
	labelCounts = {}
	for featVec in dataSet:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key]) / numEntires
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt


def createDataSet():
	dataSet = [[0, 0, 0, 0, 'no'],
			[0, 0, 0, 1, 'no'],
			[0, 1, 0, 1, 'yes'],
			[0, 1, 1, 0, 'yes'],
			[0, 0, 0, 0, 'no'],
			[1, 0, 0, 0, 'no'],
			[1, 0, 0, 1, 'no'],
			[1, 1, 1, 1, 'yes'],
			[1, 0, 1, 2, 'yes'],
			[1, 0, 1, 2, 'yes'],
			[2, 0, 1, 2, 'yes'],
			[2, 0, 1, 1, 'yes'],
			[2, 1, 0, 1, 'yes'],
			[2, 1, 0, 2, 'yes'],
			[2, 0, 0, 0, 'no']]
	labels = ['age', 'haveJob', 'haveHouse', 'creditSituation']
	return dataSet, labels

"""
Divide the data set according to the given characteristics
Parameters:
	dataSet
	axis
	value
Returns:
	
"""
def splitDataSet(dataSet, axis, value):		
	retDataSet = []
	for featVec in dataSet:
		if featVec[axis] == value:
			reducedFeatVec = featVec[:axis]
			reducedFeatVec.extend(featVec[axis+1:])
			retDataSet.append(reducedFeatVec)
	return retDataSet

"""
Select the optimal feature

Parameters:
	dataSet
Returns:
	bestFeature
"""
def chooseBestFeatureToSplit(dataSet):
	numFeatures = len(dataSet[0]) - 1
	baseEntropy = calcShannonEnt(dataSet)
	bestInfoGain = 0.0
	bestFeature = -1
	for i in range(numFeatures):
		featList = [example[i] for example in dataSet]
		uniqueVals = set(featList)
		newEntropy = 0.0
		for value in uniqueVals: 
			subDataSet = splitDataSet(dataSet, i, value)
			prob = len(subDataSet) / float(len(dataSet))
			newEntropy += prob * calcShannonEnt(subDataSet)
		infoGain = baseEntropy - newEntropy
		# print("第%d个特征的增益为%.3f" % (i, infoGain))
		if (infoGain > bestInfoGain):
			bestInfoGain = infoGain
			bestFeature = i
	return bestFeature

"""
Counts the elements in the classList that appear here the most

Parameters:
	classList
Returns:
	sortedClassCount[0][0]
"""
def majorityCnt(classList):
	classCount = {}
	for vote in classList:
		if vote not in classCount.keys():classCount[vote] = 0	
		classCount[vote] += 1
	sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)
	return sortedClassCount[0][0]

"""
Creates a decision tree

Parameters:
	dataSet
	labels
	featLabels
Returns:
	myTree
"""
def createTree(dataSet, labels, featLabels):
	classList = [example[-1] for example in dataSet]
	if classList.count(classList[0]) == len(classList):
		return classList[0]
	if len(dataSet[0]) == 1 or len(labels) == 0:
		return majorityCnt(classList)
	bestFeat = chooseBestFeatureToSplit(dataSet)
	bestFeatLabel = labels[bestFeat]
	featLabels.append(bestFeatLabel)
	myTree = {bestFeatLabel:{}}
	del(labels[bestFeat])
	featValues = [example[bestFeat] for example in dataSet]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels, featLabels)
        
	return myTree

"""
Gets the number of decision tree leaf nodes

Parameters:
	myTree
Returns:
	numLeafs
"""
def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = next(iter(myTree))
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:   numLeafs +=1
    return numLeafs

"""
Gets the number of levels in the decision tree

Parameters:
	myTree
Returns:
	maxDepth
"""
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = next(iter(myTree))
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=='dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:   thisDepth = 1
        if thisDepth > maxDepth: maxDepth = thisDepth
    return maxDepth

"""
Plot node

Parameters:
	nodeTxt
	centerPt
	parentPt
	nodeType
Returns:
	
"""
def plotNode(nodeTxt, centerPt, parentPt, nodeType):
	arrow_args = dict(arrowstyle="<-")
	font = FontProperties(fname=r"c:\windows\fonts\msyhl.ttc", size=14)
	createPlot.ax1.annotate(nodeTxt, xy=parentPt,  xycoords='axes fraction',
		xytext=centerPt, textcoords='axes fraction',
		va="center", ha="center", bbox=nodeType, arrowprops=arrow_args, fontproperties=font)

"""
Annotate the value of the directed edge attribute

Parameters:
	cntrPt、parentPt
	txtString
Returns:
	
""" 
def plotMidText(cntrPt, parentPt, txtString):
	xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]				
	yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
	createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)

"""
Plot tree

Parameters:
	myTree
	parentPt
	nodeTxt
Returns:
	
""" 
def plotTree(myTree, parentPt, nodeTxt):
	decisionNode = dict(boxstyle="sawtooth", fc="0.8")
	leafNode = dict(boxstyle="round4", fc="0.8")
	numLeafs = getNumLeafs(myTree)
	depth = getTreeDepth(myTree)
	firstStr = next(iter(myTree))
	cntrPt = (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW, plotTree.yOff)
	plotMidText(cntrPt, parentPt, nodeTxt)
	plotNode(firstStr, cntrPt, parentPt, decisionNode)
	secondDict = myTree[firstStr]
	plotTree.yOff = plotTree.yOff - 1.0/plotTree.totalD
	for key in secondDict.keys():
		if type(secondDict[key]).__name__=='dict':
			plotTree(secondDict[key],cntrPt,str(key))
		else:
			plotTree.xOff = plotTree.xOff + 1.0/plotTree.totalW
			plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntrPt, leafNode)
			plotMidText((plotTree.xOff, plotTree.yOff), cntrPt, str(key))
	plotTree.yOff = plotTree.yOff + 1.0/plotTree.totalD

"""
Create drawing panel

Parameters:
	inTree
Returns:
	
""" 
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()							
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTree.totalW = float(getNumLeafs(inTree))				
    plotTree.totalD = float(getTreeDepth(inTree))				
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;	
    plotTree(inTree, (0.5,1.0), '')								
    plt.show()													

"""
Use decision tree classification

Parameters:
	inputTree 
	featLabels
	testVec
Returns:
	classLabel
""" 
def classify(inputTree, featLabels, testVec):
	firstStr = next(iter(inputTree))
	secondDict = inputTree[firstStr]
	featIndex = featLabels.index(firstStr)	
	print("featIndex is ",featIndex)											
	for key in secondDict.keys():
		if testVec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key], featLabels, testVec)
			else: classLabel = secondDict[key]
	return classLabel

"""
Store decision tree 

Parameters:
	inputTree
	filename
Returns:

""" 
def storeTree(inputTree, filename):
	with open(filename, 'wb') as fw:
		pickle.dump(inputTree, fw)

"""
Grab decision tree 

Parameters:
	filename
Returns:
	pickle.load(fr)
""" 
def grabTree(filename):
	fr = open(filename, 'rb')
	return pickle.load(fr)


if __name__ == '__main__':
	dataSet, labels = createDataSet()
	featLabels = []
	myTree = createTree(dataSet, labels, featLabels)
	createPlot(myTree)
	print(myTree, featLabels)
	testVec = [0,0]										#测试数据
	result = classify(myTree, featLabels, testVec)
	if result == 'yes':
		print('Agree')
	if result == 'no':
		print('Refuse')