#ifndef _WIN32_WINNT            // Specifies that the minimum required platform is Windows Vista.
#define _WIN32_WINNT 0x0600     // Change this to the appropriate value to target other versions of Windows.
#endif

#include "Snap.h"
#include <iostream>
#include <fstream>

//http://snap.stanford.edu/snappy/doc/reference/index-ref.html
//http://snap.stanford.edu/class/cs224w-2012/SNAP_tutorial/tutorial.html

#define PrintInfo(x) (std::cout << #x << '\n' << x << std::endl)
inline int mod(int a, int b)
{
  return (a%b + b) % b;
}

double RandFlt()
{
  return (double)rand()/RAND_MAX;
}

class Labels {
private:
  bool * data;
  int cols;
public:
  void Create(__int64 n) {data = new bool[n*n]; memset(data, 0, n*n*sizeof(bool)); cols = n; }

  int operator()(int x, int y) {return 2*data[x + cols*y]-1; }
  void set(int x, int y, int val) {data[x + cols*y] = (val+1)/2; data[y + cols*x] = (val+1)/2; }
};

int main()
{
  srand(0);
  int n = 119287;
  double p = 0.58;
  double rp = 0.65;
  double rn = 0.20;

  PUNGraph graph = PUNGraph::New();
  for (int i=0; i<n; i++) graph->AddNode(i);

  Labels labels;
  labels.Create(n);

  for (int i=1; i<n; i++) {
    int j = i == 1 ? 0 : rand()%(i-1);
    graph->AddEdge(i, j);
    if (RandFlt() < p) labels.set(i, j, 1);
    else labels.set(i, j, -1);

    TIntV neighbors;
    TSnap::GetNodesAtHop(graph, j, 1, neighbors);
    for (int nCount=0; nCount<neighbors.Len(); nCount++) {
      int k = neighbors[nCount].Val;
      if (i == k) continue;

      if (labels(i, j) > 0) {
        if (RandFlt() < rp) {
          graph->AddEdge(i, k);
          if (labels(j, k) > 0)
            labels.set(i, k, 1);
          else
            labels.set(i, k, rand()%2 ? -1 : 1);
        }
      }
      else {
        if (labels(j, k) < 0) {
          if (RandFlt() < rn) {
            graph->AddEdge(i, k);
            labels.set(i, k, -1);
          }
        }
      }
    }
  }

  std::cout << graph->GetNodes() << std::endl;
  std::cout << graph->GetEdges() << std::endl;

  //std::ofstream stream("out.txt");
  //stream << "graph {" << std::endl;
  int * degDist = new int[n];
  memset(degDist, 0, n*sizeof(int));
  for (int i=0; i<n; i++) {
    TIntV neighbors;
    TSnap::GetNodesAtHop(graph, i, 1, neighbors);
    int sum = 0;
    for (int nCount=0; nCount<neighbors.Len(); nCount++) {
      int k = neighbors[nCount].Val;
      sum += labels(i, k);
    }
    if (sum >= 0) {
      degDist[neighbors.Len()]++;
    }
  }
  std::ofstream degStream("degP.txt");
  for (int i=0; i<n; i++) {
    if (degDist[i] != 0) {
      degStream << i << ' ' << degDist[i] << std::endl;
    }
  }
  degStream.close();

  memset(degDist, 0, n*sizeof(int));
  for (int i=0; i<n; i++) {
    TIntV neighbors;
    TSnap::GetNodesAtHop(graph, i, 1, neighbors);
    int sum = 0;
    for (int nCount=0; nCount<neighbors.Len(); nCount++) {
      int k = neighbors[nCount].Val;
      sum += labels(i, k);
    }
    if (sum < 0) {
      degDist[neighbors.Len()]++;
    }
  }
  std::ofstream degStream2("degM.txt");
  for (int i=0; i<n; i++) {
    if (degDist[i] != 0) {
      degStream2 << i << ' ' << degDist[i] << std::endl;
    }
  }
  degStream2.close();

  int nPlus = 0;
  for (int i=0; i<n; i++) {
    for (int j=i+1; j<n; j++) {
      if (graph->IsEdge(i, j)) {
        if (labels(i, j) > 0) {
          nPlus++;
          //stream << '\t' << i << " -- " << j << " [label=\"+\"];" << std::endl;
        }
        else {
          //stream << '\t' << i << " -- " << j << " [sign=\"-\"];" << std::endl;
        }
      }
    }
  }
  //stream << "}" << std::endl;
  //nPlus /= 2;
  std::cout << 100.*((double)nPlus/graph->GetEdges()) << std::endl;



  /*PNGraph graph = TSnap::LoadEdgeList<PNGraph>("email_network.txt",0,1);
  int nNodes = graph->GetNodes();
  PrintInfo(nNodes);

  PNGraph mxscc = TSnap::GetMxScc(graph);
  int nMxsccNodes = mxscc->GetNodes();
  float sccPer = (float)nMxsccNodes/nNodes;
  //PrintInfo(nMxsccNodes);
  PrintInfo(sccPer);

  PNGraph outs = TSnap::GetBfsTree(graph, mxscc->GetRndNId(), 1, 0);
  PNGraph ins = TSnap::GetBfsTree(graph, mxscc->GetRndNId(), 0, 1);

  int nOuts = outs->GetNodes() - nMxsccNodes;
  int nIns = ins->GetNodes() - nMxsccNodes;
  float outsPer = (float)nOuts/nNodes;
  float insPer = (float)nIns/nNodes;
  PrintInfo(outsPer);
  PrintInfo(insPer);
  //PrintInfo(nOuts);
  //PrintInfo(nIns);

  PNGraph alls = TSnap::GetBfsTree(graph, mxscc->GetRndNId(), 1, 1);
  int nAlls = alls->GetNodes();
  int nDisconnected = nNodes - nAlls;
  float disconnectedPer = (float)nDisconnected/nNodes;
  PrintInfo(disconnectedPer);*/

  char r;
  std::cin >> r;
}
