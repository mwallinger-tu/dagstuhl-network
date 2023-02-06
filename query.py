import requests
import networkx as nx
from bs4 import BeautifulSoup

years = ['10', '11','12', '13','14', '15','16', '17','18', '19','20', '21', '22']
min_week = 1
max_week = 52
seminars = [1,2]

G = nx.Graph()

for year in years:
    for week in range(min_week, max_week+1):
        for seminar in seminars:
            url = f"https://www.dagstuhl.de/de/seminars/seminar-calendar/seminar-details/{year}{week:02}{seminar}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            participants = soup.find("div", {"id": "participants"})

            if participants == None:
                continue

            participants = participants.find_all("li")
            p_list = []

            for participant in participants:
                p = participant.find('span')
                p_list.append(p.text.strip())
            
            for p1 in p_list:
                G.add_node(p1, name=p1)

            print(p_list)
            #print('new')
            for i1, p1 in enumerate(p_list):
                for i2, p2 in enumerate(p_list):
                    if i2 <= i1:
                        continue
                    if G.has_edge(p1, p2):
                        #print('exists')
                        G[p1][p2]['weight'] = G[p1][p2]['weight'] + 1
                    else:
                        G.add_edge(p1, p2, weight=1)

nx.write_graphml_lxml(G, "dagstuhl.graphml")