from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from datetime import datetime

class StatsWindow(QDialog):
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

        self.initUI()
        self.hide()

    def showFor(self, ip):
        self.setWindowTitle(self.title + ' - ' + ip)
        self.agent = self.main.agent_manager.agent_map[ip]
        self.txtStart.setText(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.txtEnd.setText(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        self.show()

    def initUI(self):
        self.vbLayout = QVBoxLayout()

        label_nw_time_start = QLabel('Start date:')
        self.txtStart = QLineEdit(self, placeholderText='Period start date')

        label_nw_label_nw_time_end = QLabel('End date:')
        self.txtEnd = QLineEdit(self, placeholderText='Period end date')

        self.lblUDPIn = QLabel('UDP In:')
        self.lblUDPIn.value = QLabel('')
        self.lblUDPOut = QLabel('UDP Out:')
        self.lblUDPOut.value = QLabel('')
        self.lblTCPIn = QLabel('TCP In:')
        self.lblTCPIn.value = QLabel('')
        self.lblTCPOut = QLabel('TCP Out:')
        self.lblTCPOut.value = QLabel('')

        self.btnAnalisa = QPushButton('Analyze', self)
        self.btnAnalisa.clicked.connect(self.analisa)

        self.vbLayout.addWidget(label_nw_time_start)
        self.vbLayout.addWidget(self.txtStart)
        self.vbLayout.addWidget(label_nw_label_nw_time_end)
        self.vbLayout.addWidget(self.txtEnd)
        self.vbLayout.addWidget(self.lblUDPIn)
        self.vbLayout.addWidget(self.lblUDPIn.value)
        self.vbLayout.addWidget(self.lblUDPOut)
        self.vbLayout.addWidget(self.lblUDPOut.value)
        self.vbLayout.addWidget(self.lblTCPIn)
        self.vbLayout.addWidget(self.lblTCPIn.value)
        self.vbLayout.addWidget(self.lblTCPOut)
        self.vbLayout.addWidget(self.lblTCPOut.value)
        self.vbLayout.addWidget(self.btnAnalisa)

        self.setLayout(self.vbLayout)


    def analisa(self):
        start = int(datetime.strptime(self.txtStart.text(), "%d/%m/%Y %H:%M:%S").timestamp())
        end = int(datetime.strptime(self.txtEnd.text(), "%d/%m/%Y %H:%M:%S").timestamp())

        tags = ['udpInDatagrams', 'udpOutDatagrams', 'tcpInSegs', 'tcpOutSegs']
        values = []
        for tag in tags:
            values.append(self.agent.get_data_in_time(tag, start, end))

        self.lblUDPIn.value.setText(str(values[0]))
        self.lblUDPOut.value.setText(str(values[1]))
        self.lblTCPIn.value.setText(str(values[2]))
        self.lblTCPOut.value.setText(str(values[3]))
