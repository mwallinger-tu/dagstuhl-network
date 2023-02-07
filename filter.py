import networkx as nx

G = nx.read_graphml('dagstuhl.graphml')

toRemove = []
for (u, data) in G.nodes(data=True):
    if data['type'] == "event" and data['seminar_type'] != "Dagstuhl Seminar":
        toRemove.append(u)

for u in toRemove:
    G.remove_node(u)

toRemove = []

for u in G.nodes():
    if G.degree[u] < 1:
        toRemove.append(u)

for u in toRemove:
    G.remove_node(u)



nx.write_graphml_lxml(G, "dagstuhl_filtered.graphml")

Gcc = sorted(nx.connected_components(G), key=len, reverse=True)
G0 = G.subgraph(Gcc[0])

nx.write_graphml_lxml(G0, "dagstuhl_filtered_1CC.graphml")