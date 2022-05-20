import json
import requests
import pandas as pd
import time
import glob
from collections import Counter
# DB_CONFIG = 'http://127.0.0.1:5001'
WEB_CONFIG = 'http://127.0.0.1:5002'

def get_nearest_node(x):
    # print("from get nearest node (x) : ", x)
    response = requests.get(WEB_CONFIG+'/node/userNearestNode', json = {"coordinate": [x[0],x[1]]})
    print("response.json()['node_id'] : ", response.json()['node_id'], type(response.json()['node_id']))
    return response.json()['node_id']

def get_flag(x):
        if x in intersecting_nodes:
            return True
        else:
            return False

# Loop to iterate through all of the pre-processed files containing user data
for file in glob.glob(r"preprocessedfiles\*.json"):
    print('Processing File Name ', file)
    f = open(file)
    data = json.load(f)
    print("path: ",data['path'])
    print("gps: ",len(data['gps']))
    print("gps: ",data['gps'][0])
    print("filtered_pitch: ",len(data['filtered_pitch']))
    print("filtered_pitch: ",data['filtered_pitch'][0])
    print("anchor_snapshots: ",len(data['anchor_snapshots']))
    print("pitch_rate_filtered: ",len(data['pitch_rate_filtered']))

    # change the city name accordingly when accessing the data for a different city
    city = 'Buffalo'

    # creating json for database insertion from GPS
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


    # creating json for database insertion from filtered data
    filtered_pitch_data = []
    for filtered_pitch in data['filtered_pitch']:
        filtered_pitch_data.append({
            'trip_id': data['path'],
            'timestamp': filtered_pitch['timestamp'],
            'value': filtered_pitch['value']
        })


    # creating json for database insertion from anchor_snapshots_data
    anchor_snapshots_data = []
    for snapshot in data['anchor_snapshots']:
        anchor_snapshots_data.append({
            'trip_id': data['path'],
            'timestamp': snapshot['timestamp'],
            'value': snapshot['value']
        })


    # creating json for database insertion from pitch_rate_filtered_data
    pitch_rate_filtered_data = []
    for pitch_rate in data['pitch_rate_filtered']:
        pitch_rate_filtered_data.append({
            'trip_id': data['path'],
            'timestamp': pitch_rate['timestamp'],
            'value': pitch_rate['value']
        })


    # Getting map matched data from OSRM Docker image

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
            # if i%4000==0:
            #     print('waiting for 10 seconds')
            #     time.sleep(10)
        
            coordinate_str = ";".join(all_coordinates[i:i+2])
            timestamps_specific = timestamps[i:i+2]
            radius = ['{}'.format(tolerance)]
            radius_str = ';'.join(radius*len(coordinate_str.split(';')))
            service_url = '/match/v1/driving/{}'.format(coordinate_str)
            request_url = "http://172.17.0.4" + service_url
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
    # Curating the final data set for user segmentation
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
    # all_map_matched_coordinates.to_csv('del_temp.csv',index=False)


    all_map_matched_coordinates['nearest_node_id'] = all_map_matched_coordinates['trace_coordinates'].apply(get_nearest_node)
    # all_map_matched_coordinates['nearest_node_id'] = all_map_matched_coordinates['nearest_node'].apply(lambda x: x['node_id'])
    # all_map_matched_coordinates['nearest_node_lon_lat'] = all_map_matched_coordinates['nearest_node'].apply(lambda x: x['location']['coordinates'])


    all_nodes_set = set(all_map_matched_coordinates['nearest_node_id'])
    response = requests.get(WEB_CONFIG+'/node/getIntersectingNodes', json = {"node_ids": list(all_nodes_set)})
    # print('Response is: ',response.json())

    # Logic for segmenting the user gps data
    # First get the nearest node for each of the user coordinate
    # Then get whether the nearsert nodes are intersection nodes or not
    # User data from first intersecting node ( or start of the file ) till next intersecting node belongs to 1 segment
    # The segment Id to which the data belongs is the common segment id of both the intersecting nodes

    intersecting_nodes = []
    for node in response.json():
        intersecting_nodes.append(node['node_id'])

    all_map_matched_coordinates['intersection_flag'] = False

    
    all_map_matched_coordinates['intersection_flag'] = all_map_matched_coordinates['nearest_node_id'].apply(get_flag)
    all_map_matched_coordinates['temp_segment_id'] = None
    # get inbetween nodes
    start_position = 0
    end_position = 0
    start_id = all_map_matched_coordinates.iloc[0]['nearest_node_id']
    end_id = all_map_matched_coordinates.iloc[0]['nearest_node_id']
    for i in range(1, len(all_map_matched_coordinates)):
        if all_map_matched_coordinates.iloc[i]['nearest_node_id'] in intersecting_nodes:
            if all_map_matched_coordinates.iloc[i]['nearest_node_id'] != start_id:
                end_position = i
                end_id = all_map_matched_coordinates.iloc[i]['nearest_node_id']
                # send start_id and end id
                response = requests.get(WEB_CONFIG+'/nodeSegments', json = {"node_ids": [start_id]})
                # print('start_id, end_id: ', start_id, end_id)
                segment_ids = response.json()
                response = requests.get(WEB_CONFIG+'/nodeSegments', json = {"node_ids": [end_id]})
                segment_ids.extend(response.json())
                # print('segment_ids', segment_ids)
                
                # get segment id which is coming twice
                segment_id = ''
                c_ = Counter(segment_ids)
                for key, item in c_.items():
                    if item > 1:
                        segment_id = key
                        # print("selected segment id: ", segment_id)
                        break
                if start_position == 0:
                    all_map_matched_coordinates.loc[start_position:end_position, 'temp_segment_id'] = segment_id
                else:
                    all_map_matched_coordinates.loc[start_position+1:end_position, 'temp_segment_id'] = segment_id
            # end_position = i
                start_position = end_position
                start_id = end_id

    if end_position < len(all_map_matched_coordinates):
        end_position = len(all_map_matched_coordinates)-1
        end_id = all_map_matched_coordinates.iloc[end_position]['nearest_node_id']
        # send start_id and end id
        response = requests.get(WEB_CONFIG+'/nodeSegments', json = {"node_ids": [start_id, end_id]})
        segment_ids = response.json()

        segment_id = ''
        # get segment id which is coming twice
        c_ = Counter(segment_ids)
        for key, item in c_.items():
            if item > 1:
                segment_id = key
                break
        all_map_matched_coordinates.loc[start_position+1:end_position, 'temp_segment_id'] = segment_id

    all_map_matched_coordinates.to_excel('temp_del.xlsx',index=False)

    # exit()

    trip_nodes = []
    segments = []

    # Creating the data for insertion into the GPS table data
    for gps in data['gps']:
        nearest_node_id = all_map_matched_coordinates[all_map_matched_coordinates['timestamp'] ==  gps['timestamp']]['nearest_node_id']
        map_matched_coordinate = all_map_matched_coordinates[all_map_matched_coordinates['timestamp'] ==  gps['timestamp']]['trace_coordinates']
        map_matched_longitude = map_matched_coordinate.values[0][0]
        map_matched_latitude = map_matched_coordinate.values[0][1]
        nearest_node_id = nearest_node_id.values[0].item()
        trip_nodes.append(nearest_node_id)
        segment_id = all_map_matched_coordinates[all_map_matched_coordinates['timestamp'] ==  gps['timestamp']]['temp_segment_id'].values[0]
        if segment_id not in segments and segment_id != "":
            segments.append(segment_id)
        # print('Nearest node id', nearest_node_id,type(nearest_node_id))
        gps_data.append({
            'trip_id': data['path'],
            'timestamp': gps['timestamp'],
            'system_timestamp': gps['system_timestamp'],
            'latitude': gps['lat'],
            'longitude': gps['long'],
            'map_matched_latitude': map_matched_latitude,
            'map_matched_longitude': map_matched_longitude,
            'velocity': gps['velocity'],
            'acc': gps['acc'],
            'bearing': gps['bearing'],
            'bad_data': gps['bad_data'],
            'nearest_node': nearest_node_id,
            'segment_id':segment_id
        })
        
    # response = requests.get(WEB_CONFIG+'/nodeSegments', json = {'node_ids': trip_nodes})
    # segments = response.json()

    

    #add to db
    trip_details = {
        'trip_id': data['path'],
        'city': city,
        'node_ids': list(set(trip_nodes)),
        'segment_ids': segments
        }

    #Requests to update the data base with all the user data
    response = requests.post(WEB_CONFIG+'/gps', json = gps_data)
    response = requests.post(WEB_CONFIG+'/filteredPitch', json = filtered_pitch_data)
    response = requests.post(WEB_CONFIG+'/anchorSnapshots', json = anchor_snapshots_data)
    response = requests.post(WEB_CONFIG+'/pitchRateFiltered', json = pitch_rate_filtered_data)
    response = requests.post(WEB_CONFIG+'/trip', json = [trip_details])
    # print({'trip_id': data['path'], 'segments': segments})
    response = requests.post(WEB_CONFIG+'/segment/updateTrip', json= {'trip_id': data['path'], 'segments': segments})
    print('Sending final final data to server')
    
response = requests.get(WEB_CONFIG+'/segments/getSegmentsWithTrips')
