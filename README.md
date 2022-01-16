# DATA130045.01-Graph-Data-Management-and-Mining

* In project 1, we focus on the problem of **frequent subgraph pattern mining** over a single large graph, we implement a Gspan-like algorithm with Python based on a python Gspan version, and implement a state-of-the-art subgraph matching algorithm [DP-iso](https://github.com/TrueNobi
* lity303/DP-iso) with C++ as a sub-problem.

* In project 2, we focus on the problem of **dynamic subgraph matching**, i.e. the data graph evolves over time. We propose our algorithm based on both on Success Set and Failure Set, and we also proposed an incremental Gcode algorithm for prunning with bounds for eigenvalues. 

* In project 3, we focus on the problem of **graph similarity search over a graph database**, we improved the method of Noah with Ranknet to get a better performance on top-k problem setting, i.e. to find top-k similar graphs from the graph database  to given pattern graph. Codes are inherited from the Python code of Noah, using packages of Pytorch and Pytorch-Geometric.

* In our final project, we go ahead with all our ideas in the previous three projects, and we focus on **a set of problems** which are all related to the base problem: **subgraph matching**. We show our insights that there exist close relationship with these problems (including **dynamic subgraph matching, frequent subgraph mining, similar subgraph mining, frequent similar subgraph mining**) and give our solutions to these problems, trying to apply the techniques in one problem to another, which is quite fun! Note that frequent similar subgraph mining is a new problem proposed by us, we show how we can use the solvers for other problems to solve the new problem. We also use a sample based framework for  frequent similar subgraph mining, using theories of VC-dimension and $\epsilon$-theorem with sufficient proof. 


Haha~ I've also written some blogs focusing some of the above topics, for example:

GED (Graph Edit Distance)
  * [Efficient Graph Similarity Search Over Large Graph Databases](https://truenobility303.github.io/HybridGED/)
  * [Efficient Graph Similarity Joins with Edit Distance Constraints](https://truenobility303.github.io/GSimJoin/)
MIS (Maximum Independent Set)
  * [Computing A Near-Maximum Independent Set in LinearTime by Reducing-Peeling](https://truenobility303.github.io/Reducing-Peeling/)
  * [Efficient Maximum Clique Computation over Large Sparse Graphs](https://truenobility303.github.io/MCCtoKCF/)
  * [Computing a Near-Maximum Independent Set in Dynamic Graphs](https://truenobility303.github.io/DGMIS/)
  * [Efficient Computation of a Near-Maximum Independent Set over Evolving Graphs](https://truenobility303.github.io/Dynamic-MIS/)
  * [Towards Computing a Near-Maximum Weighted Independent Seton Massive Graphs](https://truenobility303.github.io/NearMWIS/)
