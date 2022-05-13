# from djitellopy import Tello
import cv2
import drone_autopilot
import threading
import schedule ## scheduling 해서 처리?????
import requests
import time
import json
import flight.request_func as request_func
import datetime

global speed, charge_x, charge_y
global index
index = 0
speed = 1
charge_x = 0
charge_y = 0
cnt = 0

'''
drone_id를 main에서 넘겨주는 부분 필요
'''

while True:
    # data update 하는 경우에 대해서만 traj 바꾸게 설정하는게 나을 듯
    # 30분에 한 번씩 값 받아오기
    drone_id =3
    width, grape_height, height, interval, sight_range, init_point = request_func.req_droneDate(drone_id)
    traj = drone_autopilot.cpp_algo_turn(width, grape_height, height, interval, sight_range, init_point, speed)
    is_fly, start_time, end_time = request_func.req_droneControl(drone_id)
    now = datetime.datetime.now()

    # start_time = datetime.datetime.strptime('2022-03-02 19:30:00.000000', '%Y-%m-%d %H:%M:%S.%f')
    if now >= start_time:
        drone_autopilot.fly_drone(traj, charge_x, charge_y, index, drone_id)
        # print("fly drone")
    else:
        time.sleep(2) # 2 sec sleep
        continue
