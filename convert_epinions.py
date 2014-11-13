import snap

H = snap.TIntStrH()

G = snap.LoadEdgeList(snap.PNEANet, "data/epinions/soc-sign-epinions.txt", 0, 1)

for i in range(G.GetNodes()):
    H.AddDat(i, str(i))

snap.SaveGViz(G, "epinions.txt", "Directed Epinions Graph", True, H)
