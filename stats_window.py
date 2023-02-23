from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit

class StatsWindow(QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.main = parent
        self.title = 'Statistics'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.hide()

    def showFor(self, ip):
        self.setWindowTitle(self.title + ' - ' + ip)
        self.initUI()
        self.show()

    def initUI(self):
        label_nw_time_start = QLabel(self)
        label_nw_time_start.setText('inicio:')
        label_nw_time_start.setGeometry(20,20,200,30)

        line=QLineEdit(self)
        line.setGeometry(70, 20,200,30)

        label_nw_label_nw_time_end = QLabel(self)
        label_nw_label_nw_time_end.setText('fim:')
        label_nw_label_nw_time_end.setGeometry(300,20,200,30)

        line2=QLineEdit(self)
        line2.setGeometry(350, 20,200,30)

        label_udpin = QLabel(self)
        label_udpin.setText('udpin:')
        label_udpin.setGeometry(30,250,200,30)

        label_udpin.value = QLabel(self)
        label_udpin.value.setText('')
        label_udpin.value.setGeometry(30,280,200,30)

        label_udpout = QLabel(self)
        label_udpout.setText('udpout:')
        label_udpout.setGeometry(180,250,200,30)

        label_udpout.value = QLabel(self)
        label_udpout.value.setText('')
        label_udpout.value.setGeometry(180,280,200,30)

        label_tcpin = QLabel(self)
        label_tcpin.setText('tcpin:')
        label_tcpin.setGeometry(330,250,200,30)

        label_tcpin.value = QLabel(self)
        label_tcpin.value.setText('')
        label_tcpin.value.setGeometry(330,280,200,30)

        label_tecppout = QLabel(self)
        label_tecppout.setText('tcpout:')
        label_tecppout.setGeometry(480,250,200,30)

        label_tecppout.value = QLabel(self)
        label_tecppout.value.setText('')
        label_tecppout.value.setGeometry(480,280,200,30)

    def analisa(self):
        # print(line.text())
        # print(line2.text())
        #print(datetime.strptime(line.text(), "%d/%m/%Y %H:%M:%S").timestamp())
        #print(datetime.strptime(line2.text(), "%d/%m/%Y %H:%M:%S").timestamp())
        #print(TCP.get_data_in_time('tcpInSegs', datetime.strptime(line.text(), "%d/%m/%Y %H:%M:%S").timestamp(), datetime.strptime(line2.text(), "%d/%m/%Y %H:%M:%S").timestamp()))
        #print(UDP.get_data_in_time())
        pass

    def open(self):
        self.show()
