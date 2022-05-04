import os
from urllib import response
import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt

from geopy.distance import geodesic
import requests

#import constants
WEB_CONFIG = 'http://127.0.0.1:5001'
debug = True

def process_seg_gps(segment_id,df_gps, df_osm):

    num_rows_osm, num_cols_osm = df_osm.values.shape
    osm_data = df_osm.values

    #node_ids = osm_data[:, 0]
    #node_lon = osm_data[:, 1]
    #node_lat = osm_data[:, 2]

    #node_coord = osm_data[:, [2, 1]]

    num_rows_gps, num_cols_gps = df_gps.values.shape
    gps_data = df_gps.values

    if num_rows_osm < 2:
        bre = 0
        return None
    else:

        if len(gps_data) <= 4:
            return None
        else:
            vel_og = gps_data[:, 7]

            # Discard data where the car is stationary
            #if (np.count_nonzero(vel_og == 0) > 5):
             #   return None
            #else:

            sys_t_og = gps_data[:, 2]
            t_og = (gps_data[:, 1] - gps_data[0, 1]) / 1000
            coor_og = gps_data[:, [3, 4]]

            map_matched_lat = gps_data[:, 5].astype('float64')
            map_matched_lon = gps_data[:, 6].astype('float64')
            alt = np.zeros(len(map_matched_lat), )

            map_matched_coor = gps_data[:, [5, 6]]

            #x_ecef, y_ecef, z_ecef = lla_to_ecef_1(np.deg2rad(map_matched_lat), np.deg2rad(map_matched_lon), alt)


            # fig, (ax1) = plt.subplots(1)
            # ax1.plot(map_matched_lat, map_matched_lon, label="WGS")
            # # ax1.plot(acc_data[:, 1]/1000, calibrated_acc[:, 0], label="Calib-Acc")
            # # ax1.plot(gps_data[:, 0], smooth_butter(gps_data[:, 5], constants.GPS_ACC_SMOO_PARA, 2, 'lowpass'), label="GPS-ACC")
            # # ax1.plot(gps_data[:, 1]/1000, gps_data[:, 5], label="GPS-ACC")
            # ax1.legend(loc="upper left")
            # ax1.set(xlabel='Time (s)', ylabel='Raw Acc (m/s)')

            # fig, (ax1) = plt.subplots(1)
            # ax1.plot(x_ecef, y_ecef, label="ecef")
            # # ax1.plot(acc_data[:, 1]/1000, calibrated_acc[:, 0], label="Calib-Acc")
            # # ax1.plot(gps_data[:, 0], smooth_butter(gps_data[:, 5], constants.GPS_ACC_SMOO_PARA, 2, 'lowpass'), label="GPS-ACC")
            # # ax1.plot(gps_data[:, 1]/1000, gps_data[:, 5], label="GPS-ACC")
            # ax1.legend(loc="upper left")
            # ax1.set(xlabel='Time (s)', ylabel='Raw Acc (m/s)')


            acc = gps_data[:, 8]
            bearing_og = gps_data[:, 9]

            dist_vec = get_trip_dist_vec(t_og, vel_og)

            fig, (ax1) = plt.subplots(1)
            ax1.plot(t_og, vel_og, label="Vel")
            # ax1.plot(acc_data[:, 1]/1000, calibrated_acc[:, 0], label="Calib-Acc")
            # ax1.plot(gps_data[:, 0], smooth_butter(gps_data[:, 5], constants.GPS_ACC_SMOO_PARA, 2, 'lowpass'), label="GPS-ACC")
            # ax1.plot(gps_data[:, 1]/1000, gps_data[:, 5], label="GPS-ACC")
            ax1.legend(loc="upper left")
            ax1.set(xlabel='Time (s)', ylabel='Raw Acc (m/s)')

            fig, (ax1) = plt.subplots(1)
            ax1.plot(dist_vec, vel_og, label="Vel")
            #ax1.plot(acc_data[:, 1]/1000, calibrated_acc[:, 0], label="Calib-Acc")
            #ax1.plot(gps_data[:, 0], smooth_butter(gps_data[:, 5], constants.GPS_ACC_SMOO_PARA, 2, 'lowpass'), label="GPS-ACC")
            #ax1.plot(gps_data[:, 1]/1000, gps_data[:, 5], label="GPS-ACC")
            ax1.legend(loc="upper left")
            ax1.set(xlabel='Time (s)', ylabel='Raw Acc (m/s)')

            #Get the velocity data in format

            seg_velocity_data = np.hstack((np.reshape(dist_vec, (len(dist_vec), 1)), np.reshape(map_matched_coor, (len(map_matched_coor), 2)),np.reshape(vel_og, (len(vel_og), 1))))
            # print(seg_velocity_data)
            for row in seg_velocity_data:
                response = requests.post(WEB_CONFIG+'/segmentElevation/createSegmentElevationsFromAggregation', json = {"segment_id": segment_id,"distance": row[0], "latitude": row[1], "longitude": row[2], "elevation": row[3]/8})

            #d = geodesic(coor_og[0, :], coor_og[1, :]).meters

    return seg_velocity_data

def get_trip_dist_vec(t_series, vel):

    dt = np.diff(t_series)
    sampling_time = np.mean(dt)

    dist_vec = np.zeros((len(t_series), ))

    for i in range(1, len(vel)):
        dist_vec[i] = dist_vec[i-1] + vel[i-1]*sampling_time

    return dist_vec

def lla_to_ecef_1(lat, lon, alt):
    # see http://www.mathworks.de/help/toolbox/aeroblks/llatoecefposition.html
    rad = np.float64(6378137.0)        # Radius of the Earth (in meters)
    f = np.float64(1.0/298.257223563)  # Flattening factor WGS84 Model
    cosLat = np.cos(lat)
    sinLat = np.sin(lat)
    FF = (1.0-f)**2
    C = 1/np.sqrt(cosLat**2 + FF * sinLat**2)
    S = C * FF

    x = (rad * C + alt)*cosLat * np.cos(lon)
    y = (rad * C + alt)*cosLat * np.sin(lon)
    z = (rad * S + alt)*sinLat
    return x, y, z


def process_seg_data(path: str, files, folders):
    if debug:
        segment_id = path.split('/')[-1]
        print("process data: %s" % path)


    #Extract segment_id
    seg_id = os.path.basename(path)

    #Extract OSM data for this segment id
    seg_osm_file = os.path.join(path, files[0])

    df_osm = pd.read_csv(seg_osm_file, error_bad_lines=False, engine='python', skipfooter=1)

    #Iterate over all the user data that belongs to this segment

    seg_len_vec = np.zeros(1, )

    for fold in folders:
        print(fold)
        trip_fold = os.path.join(path, fold)
        trip_name = os.path.basename(trip_fold)

        #gps file

        gps_file = os.path.join(trip_fold, 'gps.csv')
        df_gps = pd.read_csv(gps_file, error_bad_lines=False, engine='python', skipfooter=1)

        seg_vel = process_seg_gps(segment_id,df_gps, df_osm)

        if seg_vel is None:
            print("Segment velocity data not available.")
        else:
            seg_file_name = trip_name + "_seg_vel.csv"
            save_path = os.path.join(path, seg_file_name)
            np.savetxt(save_path, seg_vel, fmt='%10.5f', delimiter=",")

            #seg_len_vec = np.vstack((seg_len_vec, np.reshape(len(seg_vel), (1, 1))))

    # if len(seg_len_vec) > 1:
    #     seg_len_vec = seg_len_vec[1:len(seg_len_vec), ]
    #     min_seg_len = np.min(seg_len_vec)
    # else:
    #     bre = 0




    bre = 0



def process_data_main(data_path):
    for root, folders, files in os.walk(data_path):
        if root == data_path:
            continue

        good = False
        for f in files:
            if 'nodes' in f:
                good = True
                break
        if not good:
            continue

        # TODO: check if the folder has been preprocessed before or not

        process_seg_data(root, files, folders)


if __name__ == "__main__":
    root = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(root, "output_files")
    print(path)
    process_data_main(path)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
