import os
import pandas as pd
class ParseUserData:
    allData = []
    def readFiles(userPath):
        all_trips = os.listdir(userPath)
        for trip in all_trips:
            if not trip.startswith('.'):
                all_sensors = os.listdir(userPath+trip+'/')
                print(all_sensors)
                for sensorData in all_sensors:
                    print(sensorData)
                    ParseUserData.readSensors(userPath+trip+'/'+sensorData)
                    break

    def readSensors(sensorData):
        print(sensorData)
        sensor_data_values = pd.read_csv(sensorData).to_dict('list')
        
        sensor_data_values.pop('provider', None)
        sorted(sensor_data_values, key=lambda x: int(x['sys_time']))
        # print(sensor_data_values)
        

