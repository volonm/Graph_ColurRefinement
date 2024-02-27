# Slide 1
from graph import *

G = Graph(False, 4)  # create instance G of class Graph with directed = False (so it is an undirected graph),
# 4 vertices, and label the vertices with integers (0 to 3)
print(G)  # V=[0, 2, 3, 1] (list of vertex labels)
# E=[]           (empty list = no edges)
print(G.directed)  # False
print(G.simple)  # False (default)
print(G.edges)       # empty set of instances of the Edge class
print(G.vertices)    # list of 4 instances of the Vertex class

# Slide 2
# G.vertices is a set, so we make it a (sorted) list in order to be able to index into it
# gv = sorted(list(G.vertices), key=lambda v: v.label)
# u = gv[0]       # "first" vertex of G
# print(type(u))
# print(u)        # label of the first vertex
# v = gv[1]       # "second" vertex of G
# print(v)        # label of the second vertex

# Slide 3
# w = Vertex(G)        # create instance w of class Vertex that is "related to" (but not part of!) graph G,
#                      # which means that it gets the next default label (in this case 4)
# xx = Vertex(G, 'X')  # create another vertex, but with explicit label 'X'
# print(w)             # label of vertex w
# print(xx)            # label of vertex xx
# print(G)             # G has not changed yet
# G.add_vertex(w)
# G.add_vertex(xx)
# print(G)             # now G has two more vertices (without edges)

# Slide 4
# e = Edge(u, v)       # create instance e of class Edge between vertices u and v without a weight (default);
#                      # note that, again, the edge is "related to" the graph, but not yet part of it!
# ex = Edge(u, xx, 8)
# print(e.weight)
# print(ex.weight)
# print(e)             # labels of tail and head vertices
# print(ex)
# G.add_edge(e)        # add edge e to graph G
# G += ex              # add edge ex to graph G (be careful: there is no operator + for graphs, only +=)
# print(G)             # now G finally has some edges

# Slide 5
# print(G.is_adjacent(u, v))  # should be True
# ued = u.incidence           # list of edges incident with u
# print(type(ued[0]))
# print(ued[0])
# print(ued[1])
# print(u.degree)

# Slide 6
# print(e.tail)             # label of u
# print(e.tail == u)
# print(e.head)             # label of v
# print(e.other_end(u))     # also label of v
# print(w in G.vertices)
# print(e in G.edges)
# print(v in u.neighbours)  # should be True
# print(e.incident(w))      # should be False
