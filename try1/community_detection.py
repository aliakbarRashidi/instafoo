'''
https://medium.com/labcodes/graph-databases-talking-about-your-data-relationships-with-python-b438c689dc89
Community detection using community walktrap

also https://networkx.github.io/documentation/stable/tutorial.html#analyzing-graphs
http://blog.echen.me/2012/07/31/edge-prediction-in-a-social-graph-my-solution-to-facebooks-user-recommendation-contest-on-kaggle/

'''

from py2neo import Graph
from igraph import Graph as IGraph

graph = Graph()

query = '''
MATCH (c1:Character)-[r:INTERACTS]->(c2:Character)
RETURN c1.name, c2.name, r.weight AS weight
'''

ig = IGraph.TupleList(graph.run(query), weights=True)
clusters = IGraph.community_walktrap(ig, weights="weight").as_clustering()

nodes = [{"name": node["name"]} for node in ig.vs]
for node in nodes:
    idx = ig.vs.find(name=node["name"]).index
    node["community"] = clusters.membership[idx]

write_clusters_query = '''
UNWIND {nodes} AS n
MATCH (c:Character) WHERE c.name = n.name
SET c.community = toInt(n.community)
'''
graph.run(write_clusters_query, nodes=nodes)