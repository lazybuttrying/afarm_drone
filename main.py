import sys
from PyQt5.QtWidgets import QApplication
from LoginWindow import LoginWindow
from SendVideoWindow import SendVideoWindow


class Controller:
    def __init__(self):
        pass

    def login(self):
        self.login = LoginWindow()
        self.login.cmd.connect(self.sendVideo)
        self.login.show()

    
    def sendVideo(self, userid):
        self.video = SendVideoWindow(userid)
        self.login.close()
        self.video.show()


app = QApplication(sys.argv)
view = Controller()
view.login()
sys.exit(app.exec_())
