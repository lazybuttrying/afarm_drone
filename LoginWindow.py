import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5 import uic
import requests
from Database import Database

login_page = uic.loadUiType(os.getcwd() + "/ui/login.ui")[0]

class LoginWindow(QMainWindow, login_page):
    cmd = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Afarm')
        self.setWindowIcon(QIcon(os.getcwd() + "/resource/logo.jpg"))
        self.setupUi(self)
        
        self.idText.textChanged.connect(self.idTextHandler)
        self.pwText.textChanged.connect(self.pwTextHandler)
        self.loginBtn.clicked.connect(self.loginBtnHandler)

        self.show()


    def idTextHandler(self):
        self.userid = self.idText.text()

    def pwTextHandler(self):
        self.userpw = self.pwText.text()


    @QtCore.pyqtSlot()
    def loginBtnHandler(self):
        db = Database()
        response = requests.request("POST", db.url, headers=db.headers,
                     data=db.getUser(self.userid))
        
        if response.status_code == 200:
            if response.json()["data"]["afarm_user"] == []:
                self.warning.setText("존재하지 않는 아이디입니다")
                return
            if response.json()["data"]["afarm_user"][0]["pw"] == self.userpw:
                print("Login Success")
                self.cmd.emit(self.userid)
                return
        self.warning.setText("아이디 또는 비밀번호가 일치하지 않습니다")
           


