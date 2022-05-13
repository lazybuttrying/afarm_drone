## Ex 5-1. QPushButton.

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, \
    QProgressBar, QLabel, QDesktopWidget, QMainWindow, QAction, qApp, QMenu, QMenuBar, \
        QLineEdit
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtCore import Qt

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        label1 = QLabel('Drone', self)
        label1.setAlignment(Qt.AlignCenter)
        font1 = label1.font()
        font1.setPointSize(15)
        font1.setBold(True)
        label1.setFont(font1)

        qle = QLineEdit(self)
        qle.textChanged[str].connect(self.onChanged)

        vtext = QVBoxLayout()
        vtext.addWidget(label1)
        vtext.addWidget(qle)

        btn1 = QPushButton('Send Image', self)
        btn2 = QPushButton('Clear Image', self)
        self.pbar = QProgressBar(self)
        self.step = 0
    
        vbox = QVBoxLayout()
        vbox.addWidget(vtext)
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(self.pbar)

        self.setLayout(vbox)
        self.setWindowTitle('Afarm')
        self.setGeometry(300, 300, 300, 200)
        self.show()
    
    def onChanged(self, text):
        self.lbl.setText(text)
        self.lbl.adjustSize()
    
    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())