from djitellopy import tello
import json

import cv2
from time import sleep
import requests
import datetime
import drone_autopilot
tello = tello.Tello()
tello.connect()

print(tello.get_battery())
# tello.streamon()

global save_num
save_num = 0

def load_img():
    url = "http://3.39.4.253:5000/grapeUpload?grape_id=3&quality_id=2"
    # grape_id

    img = tello.get_frame_read().frame
    img = cv2.resize(img, (360, 240))
    str = 'img' + str(save_num) + '.png'  # local에 저장됨
    # cv2.imwrite(str, img)
    save_num = save_num + 1
    # cv2.imshow("Image", img)

    cv2.waitKey(1)

    payload = {}
    files = [
        ('file', (str, img, 'image/png'))
    ]
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)

'''
drone id 받아서 _eq:drone_id 로 처리하기 ******
'''

def req_droneControl(drone_id):
    url = "https://better-rat-41.hasura.app/v1/graphql"

    payload = "{\"query\":\"query MyQuery {\\n afarm_drone(where: {id: {_eq: "+str(drone_id)+"}}) {\\n    id\\n    charge_x\\n    charge_y\\n    start_time\\n    end_time\\n    product_name\\n    product_img\\n    is_fly\\n    user_id\\n  }\\n}\\n\",\"variables\":{}}"
    headers = {
        'x-hasura-admin-secret': 'i7IqYmNWceH9bKQAtqMy5hIdujfvMQCeKjJf2JadYfFbhvXug2xatLayZB0HDFLA',
        'Content-Type': 'application/json'
    }

    Response = requests.request("POST", url, headers=headers, data=payload)
    jsonResponse = json.loads(Response.content)["data"]["afarm_drone"][0]

    is_fly = jsonResponse["is_fly"]
    # start_time = jsonResponse["start_time"]
    # end_time = jsonResponse["end_time"]
    start_time = datetime.datetime.strptime(jsonResponse["start_time"], '%Y-%m-%d %H:%M:%S.%f')
    end_time = datetime.datetime.strptime(jsonResponse["end_time"], '%Y-%m-%d %H:%M:%S.%f')

    return is_fly, start_time, end_time


def req_droneDate(drone_id):
    # conn = http.client.HTTPSConnection("better-rat-41.hasura.app")
    # payload = "{\"query\":\"query MyQuery {\\n  afarm_flight(where: {id: {_eq: 3}}) {\\n    init_x\\n    init_y\\n    width\\n    height\\n    grape_height\\n    interval\\n    sight_range\\n  }\\n}\\n\",\"variables\":{}}"
    # headers = {
    #     'x-hasura-admin-secret': 'i7IqYmNWceH9bKQAtqMy5hIdujfvMQCeKjJf2JadYfFbhvXug2xatLayZB0HDFLA',
    #     'Content-Type': 'application/json'
    # }
    # conn.request("POST", "/v1/graphql", payload, headers)
    # res = conn.getresponse()
    # data = res.read()
    #
    # jsonResponse = data.decode("utf-8")["data"]["afarm_flight"]

    url = "https://better-rat-41.hasura.app/v1/graphql"

    payload = "{\"query\":\"query MyQuery {\\n  afarm_flight(where: {id: {_eq: "+str(drone_id)+"}}) {\\n    init_x\\n    init_y\\n    width\\n    height\\n    grape_height\\n    interval\\n    sight_range\\n  }\\n}\\n\",\"variables\":{}}"
    headers = {
        'x-hasura-admin-secret': 'i7IqYmNWceH9bKQAtqMy5hIdujfvMQCeKjJf2JadYfFbhvXug2xatLayZB0HDFLA',
        'Content-Type': 'application/json'
    }

    Response = requests.request("POST", url, headers=headers, data=payload)
    jsonResponse = json.loads(Response.content)["data"]["afarm_flight"][0]

    print("Print each key-value pair from JSON response")
    # for key, value in jsonResponse.items():
    #     print(key, ":", value)

    # if jsonResponse["data_chage"]==0:
    #     pass
    # elif jsonResponse["data_chage"]==1:

    width = int(jsonResponse["width"])
    grape_height = int(jsonResponse["grape_height"])
    height = int(jsonResponse["height"])
    interval = int(jsonResponse["interval"])
    sight_range = int(jsonResponse["sight_range"])
    init_x = int(jsonResponse["init_x"])
    init_y = int(jsonResponse["init_y"])
    init_point = (init_x, init_y)

    return width, grape_height, height, interval, sight_range, init_point

def report_status(is_fly):
    url = "http://3.39.4.253:5000/qualityUpload?drone_id=3"
    print("is fly = 1")
    payload = {}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)
