from __future__ import print_function
from copy import deepcopy

class ucgraph:
	"""An undirected colored graph."""
	
	def __init__(self):
		self.neighbors={}
		self.colors={}
		self.color2vertices={}
		self.neighbors2edge={}
		self.edge2neighbors={}
		self.nextEdge=0
	
	def addEdge(self, a, b):
		if a == b:
			self.neighbors[a]=self.neighbors.get(a,set())
			return
		
		self.__updateEdgeList(a, b)
		
		if a not in self.neighbors:
			self.neighbors[a]=set()
		self.neighbors[a].add(b)
		
		if b not in self.neighbors:
			self.neighbors[b]=set()
		self.neighbors[b].add(a)
	
	def addColor(self, v, c):
		if v not in self.color2vertices and v not in self.neighbors:
			print("Warning! Setting color for missing vertex:"+str(v)+" (adding vertex)")
			self.addEdge(v,v)
		
		if v not in self.colors:
			self.colors[v]=set()
		self.colors[v].add(c)
		
		if c not in self.color2vertices:
			self.color2vertices[c]=set()
		self.color2vertices[c].add(v)
	
	def __updateEdgeList(self, a, b):
		if b not in self.neighbors.get(a,()):
			self.edge2neighbors[self.nextEdge]=frozenset([a,b])
			self.neighbors2edge[frozenset([a,b])]=self.nextEdge
			self.nextEdge=self.nextEdge+1
	
	def connectedComponents(self):
		"""breath first search"""
		islands=[]
		toExplore=set(deepcopy(self.neighbors.keys()))
		while toExplore:
			front=set([toExplore.pop()])
			island=set()
			while front:
				island=set.union(island,front)
				superFront=set.union(*[self.neighbors[v] for v in front])
				front=set.difference(superFront,island)
			toExplore=set.difference(toExplore,island)
			islands.append(island)
		return islands
	
	def topologicalOrdering(self):
		"""depth first search"""
		orderedNodes=[]
		order={}
		explored=set()
		i=0
		
		remaining=set(deepcopy(self.neighbors.keys()))
		while(remaining):
			toExplore=[remaining.pop()]
			while(toExplore):
				v=toExplore.pop()
				if v not in explored:
					explored.add(v)
					order[v]=i
					orderedNodes.append(v)
					i=i+1
				for w in self.neighbors[v]:
					if w not in explored:
						toExplore.append(w)
			remaining=set.difference(remaining,explored)
		
		return orderedNodes,order
	
	def induced(self,subset):
		"""generate the graph induced by the specified subset of vertices."""
		g=ucgraph()
		for v in subset:
			added=False
			for w in self.neighbors[v]:
				if w in subset:
					g.addEdge(v,w)
					added=True
			if not added:
				g.addEdge(v,v)
			if v in self.colors:
				for c in self.colors[v]:
					g.addColor(v,c)
		return g
	
	def cycles(self):
		"""Johnson 1975."""
		B=dict()
		blocked=dict()
		output=set()
		def CIRCUIT(v):
			def UNBLOCK(u):
				blocked[u]=False
				while B[u]:
					w = B[u].pop()
					if blocked[w]:
						UNBLOCK(w)
			
			f=False
			stack.append(v)
			blocked[v]=True
			
			for w in Ak[v]:
				if w == orderedNodes[s] and len(stack) > 2:
					output.add(frozenset(stack))
					f=True
				else:
					if not blocked[w]:
						if CIRCUIT(w):
							f=True
			if f:
				UNBLOCK(v)
			else:
				for w in Ak[v]:
					B[w].add(v)
			stack.pop()
			return f
		
		stack=[]
		orderedNodes, order=self.topologicalOrdering()
		s=0
		while s < len(orderedNodes):
			z=len(orderedNodes)
			Vk=None
			for component in self.induced(orderedNodes[s:]).connectedComponents():
				minOrder=min([order[n] for n in component])
				if minOrder<z:
					Vk=component
					z=minOrder
			if not Vk or len(Vk) < 3:
				s=s+1
				continue
			
			Ak=self.induced(Vk).neighbors
			s=z
			
			if Ak:
				for i in Ak.keys():
					blocked[i]=False
					B[i]=set()
				CIRCUIT(orderedNodes[s])
				s=s+1
			else:
				break
		
		return output
	
	def colorsByFreq(self):
		colors=[c for c in self.color2vertices]
		colors=sorted(colors,key=lambda x: len(self.color2vertices[x]))
		freqs=[len(self.color2vertices[x]) for x in colors]
		return colors,freqs
	
	def __str__(self):
		print("Neighbors:")
		print(*[(x, self.neighbors[x]) for x in self.neighbors], sep='\n')
		print("Colors:")
		print(*[(x, self.colors[x]) for x in self.neighbors], sep='\n')
		print("Color-clustered vertices:")
		print(*[(x, self.color2vertices[x]) for x in self.color2vertices], sep='\n')
