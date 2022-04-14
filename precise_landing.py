import numpy as np
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command, LocationGlobal
from pymavlink import mavutil
from opencv.lib_aruco_pose import *

import time
import math


# Define function to send landing_target mavlink message for mavlink based precision landing
# http://mavlink.org/messages/common#LANDING_TARGET
def send_land_message_v2(x_rad=0, y_rad=0, dist_m=0, time_usec=0):
    msg = vehicle.message_factory.landing_target_encode(
        time_usec,          # time target data was processed, as close to sensor capture as possible
        0,          # target num, not used
        mavutil.mavlink.MAV_FRAME_BODY_NED, # frame, not used
        x_rad,          # X-axis angular offset, in radians
        y_rad,          # Y-axis angular offset, in radians
        dist_m,          # distance, in meters
        0,          # Target x-axis size, in radians
        0,          # Target y-axis size, in radians
        0,          # x	float	X Position of the landing target on MAV_FRAME
        0,          # y	float	Y Position of the landing target on MAV_FRAME
        0,          # z	float	Z Position of the landing target on MAV_FRAME
        (1,0,0,0),  # q	float[4]	Quaternion of landing target orientation (w, x, y, z order, zero-rotation is 1, 0, 0, 0)
        2,          # type of landing target: 2 = Fiducial marker
        1,          # position_valid boolean
    )
    vehicle.send_mavlink(msg)


def marker_position_to_angle(x, y, z):
    angle_x = math.atan2(x,z)
    angle_y = math.atan2(y,z)
    return (angle_x, angle_y)

    
def camera_to_uav(x_cam, y_cam):
    x_uav = x_cam
    y_uav = y_cam
    return(x_uav, y_uav)


vehicle = connect('/dev/serial0', wait_ready=True, baud=921600) 
vehicle.parameters['PLND_ENABLED']       = 1
vehicle.parameters['PLND_TYPE']          = 2 # Mavlink landing backend 

# Camera calibration
camera_matrix = np.loadtxt("raspicam_mat.txt", delimiter=',') # TODO
camera_distortion = np.loadtxt("raspicam_dist.txt", delimiter=',') # TODO                                   
aruco_tracker = ArucoSingleTracker(
    id_to_find=72, 
    marker_size=4, #cm
    show_video=False, 
    camera_matrix=camera_matrix, 
    camera_distortion=camera_distortion
)
                
freq_send = 10 # Hz
t0 = time.time()

while True:
    marker_found, x_cm, y_cm, z_cm = aruco_tracker.track(loop=False)

    if marker_found and (time.time() >= t0 + 1.0 / freq_send):
        x_cm, y_cm          = camera_to_uav(x_cm, y_cm)
        angle_x, angle_y    = marker_position_to_angle(x_cm, y_cm, z_cm)
        
        t0 = time.time()
        print("Marker found x = {:5.0f}cm  y = {:5.0f}cm  |  angle_x = {:5f}  angle_y = {:5f}".format(x_cm, y_cm, angle_x, angle_y))
        send_land_message_v2(x_rad=angle_x, y_rad=angle_y, dist_m=z_cm*0.01, time_usec=time.time()*1e6)