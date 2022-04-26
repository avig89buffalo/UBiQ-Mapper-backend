import pandas as pd
import urllib.request
import urllib3
from urllib.request import urlopen
import json
import ast
import numpy as np
from scipy.sparse import lil_matrix
from collections import Counter
import scipy.sparse
import pickle
import json
import requests

# DB_CONFIG = 'http://127.0.0.1:5001'
WEB_CONFIG = 'http://127.0.0.1:8000'

# api = overpy.Overpass()
# (-78.8246377, 42.88402366, -78.72325793, 43.0139436)
# print('before query')

south = 42.88402366 - 0.02
west = -78.8246377 + 0.02
north = 43.0139436 + 0.02
east = -78.72325793 - 0.02
city = 'Buffalo'


way_list = []
nodes_list = []
http = urllib3.PoolManager()

q_nodes = "http://0.0.0.0:80/api/interpreter?data=[out:json];(node({},{},{},{});<;);out;".format(str(south),str(west),str(north),str(east))

response_nodes = urlopen(q_nodes)
result_nodes = json.loads(response_nodes.read())
print("OSM data done")

# with open('result_nodes.json', 'w') as f:
#     json.dump(result_nodes, f)

# types_of_roads = "motorway trunk primary secondary tertiary unclassified residential service motorway_link trunk_link primary_link secondary_link motorway_junction".split()
types_of_roads = "motorway trunk primary secondary tertiary residential service motorway_link trunk_link primary_link secondary_link motorway_junction".split()

nodes_list = []
all_road_specific_nodes = {}
way_list = []
temp_nodes_list = []
for element in result_nodes['elements']:
    if element['type'] == 'way':
        if "tags" in element:
            if "highway" in element['tags']:
                if element['tags']['highway'] in types_of_roads:
                    # all_road_specific_nodes.extend(element['nodes'])
                    for node_temp in element['nodes']:
                        all_road_specific_nodes[node_temp] = None
                    l = {'way_id': element['id'], 'node_ids':element['nodes'], 'city': city}
                    way_list.append(l)
                

# all_road_specific_nodes = list(set(all_road_specific_nodes))

for element in result_nodes['elements']:
    if element['type'] == 'node' and element['id'] in all_road_specific_nodes:
            # for sending to database
            l = {
                    'node_id': element['id'], 
                    'location':{
                        'type': 'Point',
                        'coordinates':[element['lon'],element['lat']]
                        },
                    'city': city
                }
            temp_nodes_list.append(l)
            # for local processing
            l = {'node_id': element['id'], 'latitude':element['lat'], 'longitude': element['lon'], 'city': city}
            nodes_list.append(l)

print("before sending to DB")
# pd.DataFrame(nodes_list).to_csv('data/node_list_base.csv',index=False,sep='|')
# pd.DataFrame(way_list).to_csv('data/way_list_base.csv',index=False,sep='|')

# Add to DB

response = requests.post(WEB_CONFIG+'/node', json = temp_nodes_list)
print("node done", response)
response = requests.post(WEB_CONFIG+'/way', json = way_list)
print("way done", response)


# ways = pd.read_csv(f'data/way_list_base.csv',sep='|')
# nodes = pd.read_csv(f'data/node_list_base.csv',sep='|')
                    # nodes_list_from_base
# nodes_list_from_base
# print(nodes_list)
nodes = pd.DataFrame(nodes_list)
# print(nodes.head())
ways = pd.DataFrame(way_list)
# nodes.set_index('node_id',inplace=True)
# ways['nodes'] = ways['nodes'].apply(lambda x: ast.literal_eval(x))
nodes = nodes.drop_duplicates()

all_nodes_d = ways['node_ids'].sum()
total_nodes = len(all_nodes_d)
all_nodes = set(all_nodes_d)
node_tracker = {}
counter = 0

# Here we are getting all_nodes_count
for i in all_nodes:
    node_tracker[i] = counter
    counter +=1

# Creating the matrix
list_of_all_lists = lil_matrix((total_nodes,total_nodes))

# Lets get all the intersections            
counter = Counter(all_nodes_d)

all_intersections = {}
for element in counter:
    if counter[element] > 1:
        all_intersections[element] = 0

segment_tracker = 0
for nodes_counter in range(len(ways)):
    # if nodes_counter % 100 == 0:
    #     print(nodes_counter)
    intersections = set(ways['node_ids'][nodes_counter]).intersection(all_intersections)

    for node_counter in range(len(ways['node_ids'][nodes_counter])-1):
        if (ways['node_ids'][nodes_counter][node_counter] in intersections):
            segment_tracker += 1
   
        list_of_all_lists[node_tracker[ways['node_ids'][nodes_counter][node_counter]], node_tracker[ways['node_ids'][nodes_counter][node_counter+1]]] = segment_tracker

    segment_tracker+=1

    
# with open(r"sparse_matrix.pickle", "wb") as output_file:
#     pickle.dump(list_of_all_lists, output_file)

all_sets = []
counter = 0
for nodes_counter in range(len(ways)):
    node_ids = set()
    
    for node_counter in range(len(ways['node_ids'][nodes_counter])-1):
        set_ids = {}
        from_ = ways['node_ids'][nodes_counter][node_counter]
        to_ = ways['node_ids'][nodes_counter][node_counter+1]
        segment_id = list_of_all_lists[node_tracker[from_],node_tracker[to_]]
        
        
        set_ids['segment_id'] = segment_id
        
        set_ids['node1'] = from_
        set_ids['node2'] = to_
        set_ids['index'] = counter
        counter+=1
        all_sets.append(set_ids)
    # break
    del set_ids

main_df = pd.DataFrame(all_sets)

def get_lat(x):
    try:
        return nodes['latitude'][x]
    except:
        return 'null'

def get_lon(x):
    try:
        return nodes['longitude'][x]
    except:
        return 'null'

main_df['node1_lat'] = main_df['node1'].apply(get_lat)
main_df['node1_lon'] = main_df['node1'].apply(get_lon)
main_df['node2_lat'] = main_df['node2'].apply(get_lat)
main_df['node2_lon'] = main_df['node2'].apply(get_lon)


for col in main_df.columns: #.groupby('segment_id')['']
    main_df[col] = main_df[col].astype(str)

main_df['node1_lat_lon'] = "(" + main_df['node1_lat'] +"," + main_df['node1_lon'] + ")"
main_df['node2_lat_lon'] = "(" + main_df['node2_lat'] +"," + main_df['node2_lon'] + ")"

list1 = []
current_seg = 'na'
dict_temp = {'segment_id':'','lat_lon':[]}
for row in main_df.itertuples():
    # print(row)
    if row.segment_id != current_seg:
    
        list1.append(dict_temp)
        current_seg = row.segment_id
        dict_temp = {'segment_id':row.segment_id,'nodes':[]}
        if row.node1 not in dict_temp['nodes']:
            dict_temp['nodes'].append(row.node1)

        if row.node2 not in dict_temp['nodes']:
            dict_temp['nodes'].append(row.node2)
    else:
        if row.node1_lat_lon not in dict_temp['nodes']:
            dict_temp['nodes'].append(row.node1)

        if row.node2 not in dict_temp['nodes']:
            dict_temp['nodes'].append(row.node2)
        
    # print(row.node2_lat_lon)
list1.pop(0)
    
final = pd.DataFrame(list1)
print(final.head())
segments = final['nodes'].to_list()
all_segments = []


for seg in segments:
    # all_segments.append({'node_ids': list(seg), 'city': city})
    all_segments.append({'node_ids': list(seg)})

# print(all_segments)
print("segment done")
response = requests.post(WEB_CONFIG+'/segment', json = all_segments)
print("Segment DB done", response)

segments_data = response.json()
update_nodes = []
print(segments_data[0])
print("Processing Response")
for seg in segments_data:
    segment_id = seg['_id']['$oid']
    node_ids = seg['node_ids']
    for node in node_ids:
        update_nodes.append({'node_id': node, 'segment_id': segment_id})

print("Before sending")
response = requests.post(WEB_CONFIG+'/nodeSegmentMapping', json = update_nodes)
print("after updating")