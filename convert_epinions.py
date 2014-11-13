import snap

H = snap.TIntStrH()

G = snap.LoadEdgeList(snap.PNEANet, "data/epinions/soc-pos-epinions.txt", 0, 1)

#for i in range(G.GetNodes()):
#    H.AddDat(i, str(i))

snap.SaveGViz(G, "data/epinions/epinions.dot", "Directed Epinions Graph", True, H)
