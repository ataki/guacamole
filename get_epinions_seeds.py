#!/usr/bin/python

import csv
import snap

src_f = "data/epinions/soc-sign-epinions.txt"
G = snap.LoadEdgeList(snap.PNEANet, src_f, 1, 0)

count = 0
posEdges = set()
with open(src_f) as f:
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        if row[0][0].strip() != "#":
            edge = (int(row[0]), int(row[1]))
            if int(row[2]) != -1:
                posEdges.add(edge)

topNode = 0
maxScore = -1
numNeighbors = 0

for NI in G.Nodes():
    srcId = NI.GetId()
    score = 0
    for dstId in NI.GetOutEdges():
        if (srcId, dstId) in posEdges:
            score += 1
        else:
            score -= 1
    if score > maxScore:
        maxScore = score
        numNeighbors = NI.GetOutDeg()
    topNode = srcId

print "node %d, score %d, num neighbors %d" % (topNode, maxScore, numNeighbors)
