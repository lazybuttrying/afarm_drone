import json
import os
import sys
from datetime import datetime 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import requests
import boto3

from datetime import datetime
from Database import Database
from subprocess import Popen

from dotenv import load_dotenv
load_dotenv()

send_page = uic.loadUiType(os.getcwd() + "/ui/sendVideo.ui")[0]


class SendVideoWindow(QMainWindow, send_page):

    def __init__(self, userid):
        super().__init__()
        self.userid = userid
        self.setupUi(self)
        self.setWindowTitle('Afarm')
        self.setWindowIcon(QIcon("./resource/logo.jpg"))
        self.setupUi(self)
        self.drones = {} # product_name : drone_id

        self.selectDate.addItem("드론을 선택하세요")
        self.selectDrone.currentIndexChanged.connect(self.selectDroneHandler)
        self.selectDrone_2.currentIndexChanged.connect(self.selectDrone2Handler)
        db = Database()
        response = requests.request("POST", db.url, headers=db.headers,
                                        data=db.getFlight(userid)).json()["data"]["afarm_drone"]
        
        for drone in response:
            os.makedirs("./drone/"+drone["product_name"],exist_ok=True)
            os.makedirs("./flight_info/"+drone["product_name"],exist_ok=True)
            self.selectDrone.addItem(drone["product_name"])
            self.selectDrone_2.addItem(drone["product_name"])
            self.drones[drone["product_name"]] = int(drone["id"])
            
            with open("./flight_info/"+drone["product_name"]+"/flight.json", "w") as f:
                json.dump(drone, f)

        del db
        

        # self.currentDay =  "" 
        # "2021-12-16 13:24:12" 요런 형식으로 폴더 이름 지정하고 db로 보내자
        # datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.sendBtn.clicked.connect(self.sendBtnHandler)
        self.flyBtn.clicked.connect(self.flyBtnHandler)
        # self.progressBar.reset()

        self.show()

    def selectDroneHandler(self):
        self.selectedDrone = self.selectDrone.currentText()
        self.selectDate.clear()
        date = os.listdir('./drone/' + self.selectedDrone)
        if len(date) < 1:
            self.selectDate.addItem("선택한 드론에 사진이 없습니다")
            return
        date.sort(key=lambda x: datetime.strptime(x, '%Y-%m-%d-%H-%M-%S.mp4'))
        for d in date:
            self.selectDate.addItem(d)

    def selectDrone2Handler(self):
        self.selectedDrone = self.selectDrone_2.currentText()

    def flyBtnHandler(self):
        drone_id = self.drones[self.selectedDrone]
        db = Database()
        response = {}
        with open("./flight_info/"+self.selectedDrone+"/flight.json", "r") as flight_json:
            response = json.load(flight_json)
        # response = requests.request("POST", db.url, headers=db.headers,
        #                 data=db.getFlightOne(drone_id)).json()["data"]["afarm_drone_by_pk"]
        print(response)
        Popen(["python3", "./flight/tello_api.py", 
            "--width", str(response["flight"]["width"]),
            "--height", str(response["flight"]["height"]),
            "--interval", str(response["flight"]["interval"]),
            "--drone_id", str(drone_id),
            "--drone_name",str(self.selectedDrone),
        ])
        
        
    '''
    {
  "data": {
    "afarm_drone_by_pk": {
      "start_time": "2022-03-19T13:30:00",
      "flight": {
        "init_x": 1,
        "init_y": 1,
        "width": 51,
        "height": 56,
        "interval": 1,
        "sight_range": 1,
        "grape_height": 100
      }
    }
  }
}
'''


    def sendBtnHandler(self):
                # quality upload - by folder name ("2021-12-16 13:24:12")
        # Primary key 충돌 조심하자....
        self.currentImg = 0
        date = self.selectDate.currentText()
        drone_id = self.drones[self.selectedDrone]

        db = Database()
        quality_id = requests.request("POST", db.url, headers=db.headers,
                        data=db.sendQuality(drone_id, self.userid, datetime.strptime(date,'%Y-%m-%d-%H-%M-%S.mp4'))).json()["data"]["insert_afarm_quality_one"]['id']
        print(quality_id) 

        client_s3 = boto3.client( 's3',
        aws_access_key_id = os.environ.get("S3_ACCESS_KEY"),
        aws_secret_access_key = os.environ.get("S3_SECRET_ACCESS_KEY"),
        )

        bucket_name = os.environ.get("BUCKET_NAME"),
        file = './drone/' + self.selectedDrone + '/'+date
        result = client_s3.upload_file(file, bucket_name, 'grape_before/'+str(quality_id)+".mp4")
        print(result)

        payload = "{\n\n   \"input\": \"{\\\"quality_id\\\":%s}\",\n   \"stateMachineArn\": \"arn:aws:states:ap-northeast-2:248918757327:stateMachine:AfarmProdSeoul\"\n}\n"
        response = requests.request("POST",
#             "https://3w09h26tyd.execute-api.ap-northeast-1.amazonaws.com/callStepfunction",
             "https://neizhl61lb.execute-api.ap-northeast-2.amazonaws.com/alpha",
             headers={'Content-Type': 'text/plain'},
              data=payload%(str(quality_id)))

        print(response.text)






'''
        {
"flight": {
    "init_x": 10,
    "init_y": 10,
    "width": 10,
    "height": 10,
    "interval": 1,
    "sight_range": 1,
    "grape_height": 1
},
"id": 6,
"zone": 2,
"product_name": "robomaster",
"start_time": "2022-02-09T17:30:00"
},
'''
