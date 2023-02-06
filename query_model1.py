import requests
import networkx as nx
from bs4 import BeautifulSoup
import re
from datetime import datetime

years = ['10', '11','12', '13','14', '15','16', '17','18', '19','20', '21', '22']
min_week = 1
max_week = 52
seminars = [1,2]

max_year = 2022
min_year = 2001

G = nx.Graph()

seminar_index = 0
participant_index = 0

seminar = 0
participants = {}

url = f"https://www.dagstuhl.de/de/seminars/seminar-calendar"

for year in range(max_year, max_year+1):
    request = {'form-type': 'calendar', 'year': f'{year}'}

    response = requests.post(url, json=request)

    soup = BeautifulSoup(response.text, 'html.parser')
    seminars = soup.findAll('div', {'class': 'container'})

    for seminar in seminars:
        link = seminar.find('h5')
        link = link.find('a')['href']
        
        if link == None or link == '/de':
            continue

        link = link.replace('/de/', 'https://www.dagstuhl.de/en/')
        print(link)

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')

        info = soup.find("div", {'class': 'event-details'})

        header = soup.find('header')
        definition = header.find('h5')
        name = header.find('h3')
        date = definition.find_next('h5')

        seminar_number = re.findall(r'\b\d+\b', definition.text)
        seminar_number = seminar_number[-1]

        seminar_type = definition.text.replace(seminar_number, '').strip()
        seminar_name = name.text.strip()

        if seminar_name.find('Cancelled') < 0:
            continue

        date = date.text.replace('(', '').replace(')', '').strip()
        date = date.split(',')
        year = re.findall(r'\b\d+\b|$', date[-1])[0]
        day = date[0].split('–')
        
        seminar_start = day[0].strip() + ' ' + year
        seminar_end = day[1].strip() + ' ' + year

        seminar_start = datetime.strptime(seminar_start, '%b %d %Y')
        seminar_end = datetime.strptime(seminar_end, '%b %d %Y')

        print(seminar_number)
        print(seminar_type)
        print(seminar_name)
        print(seminar_start)
        print(seminar_end)


        #participants = soup.find("div", {"id": "participants"})

        #break


nx.write_graphml_lxml(G, "dagstuhl.graphml")

