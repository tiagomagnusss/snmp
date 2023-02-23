from PyQt5.QtWidgets import QMainWindow, QLabel, QLineEdit
from datetime import datetime

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
        self.agent = None
        self.hide()

    def showFor(self, ip):
        self.setWindowTitle(self.title + ' - ' + ip)
        self.agent = self.main.agent_manager.agent_map[ip]
        self.initUI()
        self.show()

    def initUI(self):
        label_nw_time_start = QLabel(self)
        label_nw_time_start.setText('Start date:')
        self.txtStart = QLineEdit(self)

        label_nw_label_nw_time_end = QLabel(self)
        label_nw_label_nw_time_end.setText('End date:')
        self.txtEnd = QLineEdit(self)

        label_udpin = QLabel(self)
        label_udpin.setText('UDP In:')

        self.lblUDPIn.value = QLabel(self)
        self.lblUDPIn.value.setText('')

        label_udpout = QLabel(self)
        label_udpout.setText('UDP Out:')

        self.lblUDPOut.value = QLabel(self)
        self.lblUDPOut.value.setText('')

        label_tcpin = QLabel(self)
        label_tcpin.setText('TCP In:')

        self.lblTCPIn.value = QLabel(self)
        self.lblTCPIn.value.setText('')

        label_tcpppout = QLabel(self)
        label_tcpppout.setText('TCP Out:')

        self.lblTCPOut.value = QLabel(self)
        self.lblTCPOut.value.setText('')

    def analisa(self):
        start = int(datetime.strptime(self.txtStart.text(), "%d/%m/%Y %H:%M:%S").timestamp())
        end = int(datetime.strptime(self.txtEnd.text(), "%d/%m/%Y %H:%M:%S").timestamp())

        tags = ['udpInDatagrams', 'udpOutDatagrams', 'tcpInSegs', 'tcpOutSegs']
        values = []
        for tag in tags:
            values.append(self.agent.data_manager.get_data_in_time(tag, start, end))

        self.lblUDPIn.value.setText(str(values[0]))
        self.lblUDPOut.value.setText(str(values[1]))
        self.lblTCPIn.value.setText(str(values[2]))
        self.lblTCPOut.value.setText(str(values[3]))
