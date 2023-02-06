import networkx as nx

G = nx.read_graphml('dagstuhl_filtered.graphml')

toRemove = []
for (u,v, data) in G.edges(data=True):
    if data['weight'] < 2:
        toRemove.append((u,v))

for u,v in toRemove:
    G.remove_edge(u,v)

toRemove = []

for u in G.nodes():
    if G.degree[u] <= 1:
        toRemove.append(u)

for u in toRemove:
    G.remove_node(u)

nx.write_graphml_lxml(G, "dagstuhl_filtered2.graphml")
nx.write_gml(G, 'dagstuhl.gml')