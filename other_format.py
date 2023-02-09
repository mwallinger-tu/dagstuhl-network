import networkx as nx
from datetime import datetime


GCC = nx.read_graphml('dagstuhl_filtered_1CC.graphml')
cutoff_year = 2019

G = nx.Graph()

for node, data in GCC.nodes(data=True):
    if data['type'] == 'event' and data['seminar_start']:
        dt = datetime.strptime(data['seminar_start'], "%Y-%m-%d")

        if dt.year < cutoff_year:
            continue

        toConnect = []
        for n in GCC.neighbors(node):
            #print(n)
            if G.has_node(n):
                G.nodes[n]['attendence'] = G.nodes[n]['attendence'] + 1
            else:
                G.add_node(n, name=n, attendence=1)
            toConnect.append(n)

        for i1, n1 in enumerate(toConnect):
            for i2, n2 in enumerate(toConnect):
                if i2 <= i1:
                    continue

                if G.has_edge(n1,n2):
                    G[n1][n2]['weight'] = G[n1][n2]['weight'] +1
                else:
                    G.add_edge(n1,n2, weight=1)


nx.write_graphml_lxml(G, f"dagstuhl_people_{cutoff_year}.graphml")

toRemove = []
for node,data  in G.nodes(data=True):
    if data['attendence'] <= 1:
        toRemove.append(node)

for n in toRemove:
    G.remove_node(n)

print(len(G.nodes()), len(G.edges()))

nx.write_graphml_lxml(G, f"dagstuhl_people_{cutoff_year}_no_deg1.graphml")