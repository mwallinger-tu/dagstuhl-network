import requests
import networkx as nx
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time

years = ['10', '11','12', '13','14', '15','16', '17','18', '19','20', '21', '22']
min_week = 1
max_week = 52
seminars = [1,2]

max_year = 2022
min_year = 1990

G = nx.Graph()

seminar_index = 0
participant_index = 0

seminar = 0
participants = {}

def query_seminar(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    info = soup.find("div", {'class': 'event-details'})

    header = info.find('header')
    definition = header.find('h5')
    name = header.find('h3')
    date = definition.find_next('h5')

    seminar_number = re.findall(r'\b\d+\b', definition.text)
    seminar_number = seminar_number[-1]

    seminar_type = definition.text.replace(seminar_number, '').strip()
    seminar_name = name.text.strip()

    if seminar_name.find('Cancelled') >= 0 or seminar_name.find('Postponed') >= 0:
        return None, None, None, None, None, None, None, None, None, None, None, None, None, None

    date = date.text.replace('(', '').replace(')', '').strip()
    date = date.split(',')
    year = re.findall(r'\b\d+\b|$', date[-1])[0]
    day = date[0].split('–')
    
    seminar_start = day[0].strip() + ' ' + year
    seminar_end = day[1].strip() + ' ' + year

    seminar_start = datetime.strptime(seminar_start, '%b %d %Y').strftime('%Y-%m-%d')
    seminar_end = datetime.strptime(seminar_end, '%b %d %Y').strftime('%Y-%m-%d')
    seminar_permalink = f"https://www.dagstuhl.de/{seminar_number}"

    # info.find('')
    # print(seminar_number)
    # print(seminar_type)
    # print(seminar_name)
    # print(seminar_start)
    # print(seminar_end)    
    
   
    ###
    # Organizers
    ###
    organizers = info.find('h5', string='Organizers')
    organizer_list = []
    
    if not organizers:
        organizers = info.find('h5', string='Organizer')

    if organizers:
        organizers = organizers.parent.parent.find_all("li")

        for organizer in organizers:
            name_span = organizer.find('span')
            institute_span = name_span.find_next_sibling('span')
            dblp = name_span.find_next_sibling('a')
            
            if dblp:
                dblp = dblp['href']
            else:
                dblp = ''
            
            if institute_span:
                inst = institute_span.text
                
                inst = inst[1:-2].strip()
                inst_split = inst.split(',')
            
                country = inst_split[-1].strip()
                institute = inst_split[0].strip()
            else:
                country = ''
                institute = ''
            
            
            name = name_span.text.strip()
            organizer_list.append((name, country, institute, dblp))
    
    motivation = info.find('h5', string=lambda t: t and 'Motivation' in t)
    
    ###
    # Summary
    ###
    summary = info.find_all('h5')
    found = False

    for s in summary:
        if 'Summary' in s.text:
            summary = s
            found = True
            break

    if found:
        summary = summary.parent.parent.find('div',  {'class': 'section-content'}).find_next_sibling()
        seminar_summary = ' '.join([str(e) for e in summary.contents])
    else:
        seminar_summary = ""
    
    ###
    # Motivation
    ###
    motivation = info.find_all('h5')
    found = False

    for s in motivation:
        if 'Motivation' in s.text:
            motivation = s
            found = True
            break

    if found and motivation.parent.parent != None:
        motivation = motivation.parent.parent.find('div',  {'class': 'section-content'}).find_next_sibling()
        seminar_motivation = ' '.join([str(e) for e in motivation.contents])
    else:
        seminar_motivation = ""
    
        
    ###
    # Related Seminars
    ###
    related = info.find('h5', string='Related Seminars')
    related_seminars = []
    if related:
        related_sems = related.parent.parent.find_all('li')
        
        for sem in related_sems:
            sem_number = re.findall(r'\b\d+\b', sem.text)
            sem_number = seminar_number[0]
            related_seminars.append(sem_number)
            
    ###
    # Publications
    ###
    publications = info.find('h5', string='Publications')
    seminar_publications = []

    if publications:
        publications = publications.parent.parent.find_all('li')
        
        for publication in publications:
            doi = publication.find("a")
            
            if doi:
                seminar_publications.append(doi['href'])
            
    ###
    # Impacts
    ###
    impacts = info.find('h5', string='Impacts')
    seminar_impacts = []

    if impacts:
        impacts = impacts.parent.parent.find_all('li')
        
        for impact in impacts:
            doi = impact.find("a")
            
            if doi:
                seminar_impacts.append(doi['href'])
            
    ###
    # Classification
    ###
    classification = info.find('h5', string='Classification')
    seminar_classification = []

    if classification:
        classification = classification.parent.parent.find_all('li')
        
        for keyword in classification:
            seminar_classification.append(keyword.text)
    
    ###
    # Keywords
    ###
    keywords = info.find('h5', string='Keywords')
    seminar_keywords = []

    if keywords:
        keywords = keywords.parent.parent.find_all('li')
        
        for keyword in keywords:
            seminar_keywords.append(keyword.text)
    
    ###
    # Participants
    ###
    participants_dict = {}
    participants_html = soup.find("div", {'id': 'participants'})
    
    if participants_html == None:
        print('no participants')
    else:
        ishybrid = False       
        onsite = participants_html.find(string='On-site')
        if onsite != None:
            onsite = onsite.parent.parent
            ishybrid = True
            participants = onsite.find_all("li")

            for participant in participants:
                name_span = participant.find('span')
                institute_span = name_span.find_next_sibling('span')
                dblp = name_span.find_next_sibling('a')
                
                name = name_span.text.strip()
                
                if dblp:
                    dblp = dblp['href']
                else:
                    dblp = ''
                
                if institute_span:
                    inst = institute_span.text.strip()
                    
                    inst = inst[1:-2].strip()
                    inst_split = inst.split(',')
                
                    country = inst_split[-1].strip()
                    institute = inst_split[0].strip()
                else:
                    country = ''
                    institute = ''
                
                #print(name, institute, country, dblp)
                participants_dict[name] = {'institute': institute, 'country': country, 'dblp': dblp, 'onsite': True, 'isOrganizer': False}
            
        remote = participants_html.find(string='Remote:')
        if remote != None:
            ishybrid = True
            remote = remote.parent.parent       
            participants = remote.find_all("li")

            for participant in participants:
                name_span = participant.find('span')
                institute_span = name_span.find_next_sibling('span')
                dblp = name_span.find_next_sibling('a')
                
                name = name_span.text.strip()
                
                if dblp:
                    dblp = dblp['href']
                else:
                    dblp = ''
                
                if institute_span:
                    inst = institute_span.text.strip()
                    
                    inst = inst[1:-2].strip()
                    inst_split = inst.split(',')
                
                    country = inst_split[-1].strip()
                    institute = inst_split[0].strip()
                else:
                    country = ''
                    institute = ''
                
                #print(name, institute, country, dblp)
                participants_dict[name] = {'institute': institute, 'country': country, 'dblp': dblp, 'onsite': False, 'isOrganizer': False}

        if not ishybrid:
            participants = participants_html.find_all("li")

            for participant in participants:
                name_span = participant.find('span')
                institute_span = name_span.find_next_sibling('span')
                dblp = name_span.find_next_sibling('a')
                
                name = name_span.text.strip()
                
                if dblp:
                    dblp = dblp['href']
                else:
                    dblp = ''
                
                if institute_span:
                    inst = institute_span.text
                    
                    inst = inst[1:-2].strip()
                    inst_split = inst.split(',')
                
                    country = inst_split[-1].strip()
                    institute = inst_split[0].strip()
                else:
                    country = ''
                    institute = ''
                
                #print(name, institute, country, dblp)
                participants_dict[name] = {'institute': institute, 'country': country, 'dblp': dblp, 'onsite': True, 'isOrganizer': False}

    
    for name, country, institute, dblp in organizer_list:
        if name in participants_dict:
            participants_dict[name]['isOrganizer'] = True
        else:
            participants_dict[name] = {'institute': institute, 'country': country, 'dblp': dblp, 'onsite': True, 'isOrganizer': True, 'missingOrganizer': True}
    
    return seminar_number, seminar_type, seminar_name, seminar_start, seminar_end, seminar_permalink, seminar_motivation, seminar_summary, participants_dict, seminar_impacts, seminar_publications, seminar_classification, seminar_keywords, related_seminars


def query_year(url, year):
    '''
    Query a given year of the seminar calendar and return a list of links to individual seminars
    '''
    
    request = {'form-type': 'calendar', 'year': f'{year}'}

    response = requests.post(url, json=request)

    soup = BeautifulSoup(response.text, 'html.parser')
    seminars = soup.findAll('div', {'class': 'container'})
    
    seminar_list = []

    for seminar in seminars:
        link = seminar.find('h5')
        link = link.find('a')['href']
        
        if link == None or len(link) <= 10:
            continue

        link = link.replace('/en/', 'https://www.dagstuhl.de/en/')
        seminar_list.append(link)
        
    return seminar_list
        
def query():
    url = f"https://www.dagstuhl.de/de/seminars/seminar-calendar"
    
    for year in range(max_year, max_year+1):
        seminar_list = query_year(url, year)
        
        for seminar in seminar_list:
            print(seminar)
    
def main():
    #query()
    
    G = nx.Graph()
    
    for year in range(min_year, max_year + 1):
        print(f'processing year: {year}')
        seminars = query_year('https://www.dagstuhl.de/en/seminars/seminar-calendar', year)
    
        for seminar_link in seminars:
            print(seminar_link)
            
            seminar_number, seminar_type, seminar_name, seminar_start, seminar_end, seminar_permalink, seminar_motivation, seminar_summary, seminar_participants, seminar_impacts, seminar_publications, seminar_classification, seminar_keywords, related_seminars = query_seminar(seminar_link)
            
            if seminar_number == None:
                continue
            
            seminar_impacts = '; '.join([str(e) for e in seminar_impacts])
            seminar_publications = '; '.join([str(e) for e in seminar_publications])
            seminar_classification = '; '.join([str(e) for e in seminar_classification])
            seminar_keywords = '; '.join([str(e) for e in seminar_keywords])
            related_seminars = '; '.join([str(e) for e in related_seminars])
            
            G.add_node(seminar_number, type="event", seminar_number=seminar_number, seminar_type=seminar_type, seminar_name= seminar_name, seminar_start= seminar_start, seminar_end=seminar_end, seminar_permalink= seminar_permalink, seminar_motivation= seminar_motivation, seminar_summary= seminar_summary, seminar_impacts= seminar_impacts, seminar_publications= seminar_publications, seminar_classification= seminar_classification, seminar_keywords=seminar_keywords, seminar_related=related_seminars)

            for name, info in seminar_participants.items():
                if not G.has_node(name):
                    G.add_node(name, name=name, type="person", dblp=info['dblp'])

                G.add_edge(seminar_number, name, institute=info['institute'], country=info['country'], onsite=info['onsite'], is_organizer=info['isOrganizer'])

                
            time.sleep(0.2)
            
            # print(G.nodes(data=True))
            # print(G.edges(data=True))
        
    nx.write_graphml_lxml(G, "dagstuhl.graphml")
    
if __name__ == '__main__':
    main()





