# dagstuhl graph

Network of events and people at Dagstuhl. All networks were created from publicly available data. 

## Network Formats and data:

The base graph (dagstuhl.graphml) represents a network of all recorded events and people from 1990 onwards. The graph contains two types of nodes ('events' and 'person') with different data attributes attached. Edges are present if a person attended an event. Note that not all attributes are always present:

**Both**: 
- type: {'event', 'person'}

**Event**: 

- **seminar_number**: string
- **seminar_name**: string
- **seminar_type**: string (e.g. 'Dagstuhl Seminar)
- **seminar_start**: ISO-string (e.g. 2011-05-15)
- **seminar_end**: ISO-string
- **seminar_summary**: string (e.g. usually a long text) 
- **seminar_motivation**: string (e.g. usually a long text)
- **seminar_impacts**: string **;**-separated (e.g. "link1;link2;link3", usually links to publications)
- **seminar_related**: string **;**-separated (e.g. "link1;link2;link3", usually links to other seminars)
- **seminar_publications**: string **;**-separated (e.g. "link1;link2;link3", usually dplb links) 
- **seminar_classification**: string **;**-separated (e.g. "classification1;classification2")
- **seminar_keywords**: string **;**-separated (e.g. "keyword1;keyword1")

**Person**: 

- **name**: string
- **dblp**: string (dblp url)


**Edge**:

is_organizer: boolean
onsite: boolean
institute: string (e.g. TU Wien)
country: string (e.g. AT)

Furthermore, participant information is not available before 2000. Only the organizers are stated and thus in the graph. graphml** 

## Available graphs:

**dagstuhl.graphml** is the full graph. **dagstuhl_filtered.graphml** only has events of type "Dagstuhl Seminar". Furthermore, all people that only attended a single seminar are removed. Next, **dagstuhl_filtered_1CC.graphml** only retains the largest connected component. 

Lastly, a second view is available where nodes of type "event" are removed and people are connected if they attended a "Dagstuhl Seminar" together. **dagstuhl_people.graphml** contains all people from 1990 onwards. **dagstuhl_people_{year}.graphml** is a filtered graph from a given {year} onwards. 

## Filter the graph yourself

See *filter.py* and *other_format.py* on how filtering the graph for your own purpose works.