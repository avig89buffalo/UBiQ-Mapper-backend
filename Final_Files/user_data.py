import json
import requests
import pandas as pd
import time 

DB_CONFIG = 'http://127.0.0.1:5001'

f = open('json_data.json')
data = json.load(f)
print("path: ",data['path'])
print("gps: ",len(data['gps']))
print("gps: ",data['gps'][0])
print("filtered_pitch: ",len(data['filtered_pitch']))
print("filtered_pitch: ",data['filtered_pitch'][0])
print("anchor_snapshots: ",len(data['anchor_snapshots']))
print("pitch_rate_filtered: ",len(data['pitch_rate_filtered']))

city = 'Buffalo'

gps_data = []
gps_processing = []
for gps in data['gps']:
    # gps_data.append({
    #     'trip_id': data['path'],
    #     'timestamp': gps['timestamp'],
    #     'system_timestamp': gps['system_timestamp'],
    #     'latitude': gps['lat'],
    #     'longitude': gps['long'],
    #     'velocity': gps['velocity'],
    #     'acc': gps['acc'],
    #     'bearing': gps['bearing'],
    #     'bad_data': gps['bad_data']
    # })
    gps_processing.append({
        'timestamp': gps['timestamp'],
        'latitude': gps['lat'],
        'longitude': gps['long']
    })



filtered_pitch_data = []
for filtered_pitch in data['filtered_pitch']:
    filtered_pitch_data.append({
        'trip_id': data['path'],
        'timestamp': filtered_pitch['timestamp'],
        'value': filtered_pitch['value']
    })



anchor_snapshots_data = []
for snapshot in data['anchor_snapshots']:
    anchor_snapshots_data.append({
        'trip_id': data['path'],
        'timestamp': snapshot['timestamp'],
        'value': snapshot['value']
    })



pitch_rate_filtered_data = []
for pitch_rate in data['pitch_rate_filtered']:
    pitch_rate_filtered_data.append({
        'trip_id': data['path'],
        'timestamp': pitch_rate['timestamp'],
        'value': pitch_rate['value']
    })


gps_data_points_all = pd.DataFrame(gps_processing)
# print(gps_data_points_all)
Ld = []
all_coordinates = (gps_data_points_all['longitude'].astype(str)+","+gps_data_points_all['latitude'].astype(str)).tolist()
timestamps = gps_data_points_all['timestamp'].copy()
for tolerance in [50, 40, 30, 20, 10]:
# for tolerance in [50]:
    # print(tolerance)
    # print(len(all_coordinates))
    for i in range(0, len(all_coordinates)-2, 2):
        if i%4000==0:
            print('sleeping for 10 seconds')
            time.sleep(10)
    
        coordinate_str = ";".join(all_coordinates[i:i+2])
        timestamps_specific = timestamps[i:i+2]
        radius = ['{}'.format(tolerance)]
        radius_str = ';'.join(radius*len(coordinate_str.split(';')))
        service_url = '/match/v1/driving/{}'.format(coordinate_str)
        request_url = "http://127.0.0.1:5000" + service_url
        payload = {'geometries': 'geojson', 'steps': 'false', 'radiuses': radius_str}

        r = requests.get(request_url, params=payload)
        
        results = r.json()
        try:
            for tracepoint, coordinate, timestamps_temp in zip(results['tracepoints'], coordinate_str.split(';'), timestamps_specific):
                coordinate = coordinate.split(',')
                # print(tracepoint['location'][0], tracepoint['location'][1]) # lon, lat
                dict1 = {}
                dict1['trace_lon'] = tracepoint['location'][0]
                dict1['trace_lat'] = tracepoint['location'][1]
                dict1['distance'] = tracepoint['distance']
                dict1['user_lon'] = coordinate[0]
                dict1['user_lat'] = coordinate[1]
                dict1['timestamp'] = timestamps_temp
                 # print(dict1)
                Ld.append(dict1)
        except:
            print('got error')
            print(results)


        coordinate_str = ";".join(all_coordinates[len(all_coordinates)-2:])
        timestamps_specific = timestamps[len(all_coordinates)-2:]
        radius = ['{}'.format(tolerance)]
        radius_str = ';'.join(radius*len(coordinate_str.split(';')))
        service_url = '/match/v1/driving/{}'.format(coordinate_str)
        request_url = "http://127.0.0.1:5000" + service_url
        payload = {'geometries': 'geojson', 'steps': 'false', 'radiuses': radius_str}

        r = requests.get(request_url, params=payload)
        
        results = r.json()
        
        try:
            for tracepoint, coordinate, timestamps_temp in zip(results['tracepoints'], coordinate_str.split(';'), timestamps_specific):
                coordinate = coordinate.split(',')
                # print(tracepoint['location'][0], tracepoint['location'][1]) # lon, lat
                dict1 = {}
                dict1['trace_lon'] = tracepoint['location'][0]
                dict1['trace_lat'] = tracepoint['location'][1]
                dict1['distance'] = tracepoint['distance']
                dict1['user_lon'] = coordinate[0]
                dict1['user_lat'] = coordinate[1]
                dict1['timestamp'] = timestamps_temp
                 # print(dict1)
                Ld.append(dict1)
        except:
            print('got error')
            print(results)

# print('Ld', len(Ld))
all_map_matched_coordinates = pd.DataFrame(Ld)
all_map_matched_coordinates['user_coordinates'] = all_map_matched_coordinates['user_lon'].astype(str)+" , "+all_map_matched_coordinates['user_lat'].astype(str)
all_map_matched_coordinates['trace_coordinates'] = all_map_matched_coordinates['trace_lon'].astype(str)+" , "+all_map_matched_coordinates['trace_lat'].astype(str)

all_map_matched_coordinates.sort_values(['timestamp','user_coordinates','distance'],inplace=True)
all_map_matched_coordinates.reset_index(inplace=True, drop=True)
# all_map_matched_coordinates.to_csv('FINAL_all_map_matched_coordinates.csv',index=False)


all_map_matched_coordinates.drop_duplicates(subset=['user_coordinates','timestamp'], keep  = 'first',inplace=True)
all_map_matched_coordinates.reset_index(inplace=True, drop=True)
# all_map_matched_coordinates.to_csv('FILTERED_FINAL_all_map_matched_coordinates.csv',index=False)

all_map_matched_coordinates['user_coordinates'] = all_map_matched_coordinates['user_coordinates'].apply(lambda x: [float(x.split(',')[0].strip()),float(x.split(',')[1].strip())])
all_map_matched_coordinates['trace_coordinates'] = all_map_matched_coordinates['trace_coordinates'].apply(lambda x: [float(x.split(',')[0].strip()),float(x.split(',')[1].strip())])

print('all_map_matched_coordinates ', len(all_map_matched_coordinates))
all_map_matched_coordinates.to_csv('del_temp.csv',index=False)

def get_nearest_node(x):
    response = requests.get(DB_CONFIG+'/node/userNearestNode', json = {"coordinate": [x[0],x[1]]})
    # print(response.json())
    return response.json()['node_id']


all_map_matched_coordinates['nearest_node_id'] = all_map_matched_coordinates['trace_coordinates'].apply(get_nearest_node)
# all_map_matched_coordinates['nearest_node_id'] = all_map_matched_coordinates['nearest_node'].apply(lambda x: x['node_id'])
# all_map_matched_coordinates['nearest_node_lon_lat'] = all_map_matched_coordinates['nearest_node'].apply(lambda x: x['location']['coordinates'])
all_map_matched_coordinates.to_excel('temp_del.xlsx',index=False)
trip_nodes = []

for gps in data['gps']:
    nearest_node_id = all_map_matched_coordinates[all_map_matched_coordinates['timestamp'] ==  gps['timestamp']]['nearest_node_id']
    nearest_node_id = nearest_node_id.values[0].item()
    trip_nodes.append(nearest_node_id)
    # print('Nearest node id', nearest_node_id,type(nearest_node_id))
    gps_data.append({
        'trip_id': data['path'],
        'timestamp': gps['timestamp'],
        'system_timestamp': gps['system_timestamp'],
        'latitude': gps['lat'],
        'longitude': gps['long'],
        'velocity': gps['velocity'],
        'acc': gps['acc'],
        'bearing': gps['bearing'],
        'bad_data': gps['bad_data'],
        'nearest_node': nearest_node_id
    })
    
response = requests.get(DB_CONFIG+'/nodeSegments', json = {'node_ids': trip_nodes})
segments = response.json()

#add to db
trip_details = {
    'trip_id': data['path'],
    'city': city,
    'node_ids': list(set(trip_nodes)),
    'segment_ids': segments
    }

response = requests.post(DB_CONFIG+'/gps', json = gps_data)
response = requests.post(DB_CONFIG+'/filteredPitch', json = filtered_pitch_data)
response = requests.post(DB_CONFIG+'/anchorSnapshots', json = anchor_snapshots_data)
response = requests.post(DB_CONFIG+'/pitchRateFiltered', json = pitch_rate_filtered_data)
response = requests.post(DB_CONFIG+'/trip', json = [trip_details])