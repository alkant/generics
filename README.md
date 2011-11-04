# Summary

Generic algorithms for python. Only simple graph theoretic algorithms for now.

# Graphs

``ucgraph.py`` is an Undirected Colored Graph library: your usual undirected unweighted graph where nodes can hold a set of attributes (colors). Nodes can be any python object.

## Features

* Topological ordering,
* Connected components search,
* Induced graph of selected vertices,
* Cycles enumeration (Johnson 1975).

## Usage example

	>>> import ucgraph
	
	>>> g=ucgraph.ucgraph()
	
	>>> g.addEdge(0,1)
	>>> g.addEdge(1,'e')
	>>> g.addEdge('hi','there')
	
	>>> g.connectedComponents()
	[set([0, 1, 'e']), set(['hi', 'there'])]

