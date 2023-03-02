import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from datetime import datetime

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class StatsWindow(QDialog):
    def __init__(self, parent):
        super().__init__()
        self.main = parent
        self.title = 'Statistics'
        self.left = 100
        self.top = 100
        self.width = 1200
        self.height = 570
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.agent = None

        self.initUI()
        self.hide()

    def showFor(self, ip):
        self.setWindowTitle(self.title + ' - ' + ip)
        self.agent = self.main.agent_manager.agent_map[ip]
        self.update_plot()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()
        self.show()

    def initUI(self):
        self.vbLayout = QVBoxLayout()
        self.lblInErrors = QLabel('Porcentagem de erros na entrada:')
        self.lblOutErrors = QLabel('Porcentagem de erros na saída:')
        self.lblInDiscards = QLabel('Porcentagem de descarte na entrada:')
        self.lblOutDiscards = QLabel('Porcentagem de descarte na saída:')
        self.lblifOutQLen = QLabel('Pacotes na fila de saída:')

        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)

        self.vbLayout.addWidget(self.canvas)
        self.vbLayout.addStretch(1)

        self.vbLayout.addWidget(self.lblInErrors)
        self.vbLayout.addWidget(self.lblOutErrors)
        self.vbLayout.addWidget(self.lblInDiscards)
        self.vbLayout.addWidget(self.lblOutDiscards)
        self.vbLayout.addWidget(self.lblifOutQLen)

        self.setLayout(self.vbLayout)


    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        #self.zdata = self.zdata[1:] + [random.randint(0, 5)]

        ifInUcastPkts = float(self.agent.data_map['ifInUcastPkts'][len(self.agent.data_map['ifInUcastPkts']) - 1]['value'])
        ifInNUcastPkts = float(self.agent.data_map['ifInNUcastPkts'][len(self.agent.data_map['ifInNUcastPkts']) - 1]['value'])
        ifInErrors = float(self.agent.data_map['ifInErrors'][len(self.agent.data_map['ifInErrors']) - 1]['value'])
        ifOutErrors = float(self.agent.data_map['ifOutErrors'][len(self.agent.data_map['ifOutErrors']) - 1]['value'])
        ifInDiscards = float(self.agent.data_map['ifInDiscards'][len(self.agent.data_map['ifInDiscards']) - 1]['value'])
        ifOutDiscards = float(self.agent.data_map['ifOutDiscards'][len(self.agent.data_map['ifOutDiscards']) - 1]['value'])
        ifOutQLen = int(self.agent.data_map['ifOutQLen'][len(self.agent.data_map['ifOutQLen']) - 1]['value'])

        self.lblInErrors.setText('Porcentagem de erros na entrada: ' + str(ifInErrors/(ifInUcastPkts+ifInNUcastPkts)) + '%')
        self.lblOutErrors.setText('Porcentagem de erros na saída: ' + str(ifOutErrors/(ifInUcastPkts+ifInNUcastPkts)) + '%')
        self.lblInDiscards.setText('Porcentagem de descarte na entrada: ' + str(ifInDiscards/(ifInUcastPkts+ifInNUcastPkts)) + '%')
        self.lblOutDiscards.setText('Porcentagem de descarte na saída: ' + str(ifOutDiscards/(ifInUcastPkts+ifInNUcastPkts)) + '%')
        self.lblifOutQLen.setText('Pacotes na fila de saída: ' + str(ifOutQLen) + 'pkts')

        time_stamp = []
        dataTotal = []

        if len(self.agent.data_map['ifInOctets']) > 2 and len(self.agent.data_map['ifInOctets']) <= 30:
           for x in range(1, len(self.agent.data_map['ifInOctets'])):
               time_stamp.append(datetime.fromtimestamp(int(self.agent.data_map['ifInOctets'][x]['timestamp'])))

               dataIn = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
               dataOut = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
               data = dataIn + dataOut
               time_diff = int(self.agent.data_map['ifInOctets'][x]['timestamp']) - int(self.agent.data_map['ifInOctets'][x-1]['timestamp'])
               dataTotal.append((1/(10*time_diff))*8*(data))

        if len(self.agent.data_map['ifInOctets']) > 30:
           for x in range(len(self.agent.data_map['ifInOctets']) - 30, len(self.agent.data_map['ifInOctets'])):
               time_stamp.append(datetime.fromtimestamp(int(self.agent.data_map['ifInOctets'][x]['timestamp'])))

               dataIn = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
               dataOut = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
               data = dataIn + dataOut
               time_diff = int(self.agent.data_map['ifInOctets'][x]['timestamp']) - int(self.agent.data_map['ifInOctets'][x-1]['timestamp'])
               dataTotal.append((1/(10*time_diff))*8*(data))

        # print('size ---------------------------')
        # print(len(self.agent.data_map['ifInOctets']))
        # print('time ---------------------------')
        # print(time_stamp)
        # print('data ---------------------------')
        # print(dataTotal)

        self.canvas.axes.cla()  # Clear the canvas.
        date_fmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        self.canvas.axes.xaxis.set_major_formatter(date_fmt)
        self.canvas.axes.yaxis.label.set_text('kbps')
        self.canvas.axes.xaxis.set_major_formatter(date_fmt)
        for label in self.canvas.axes.xaxis.get_ticklabels(which='major'):
            label.set(rotation=8, fontsize=8)

        self.canvas.axes.grid(True, color='k', linestyle='-', linewidth=0.05)
        self.canvas.axes.plot(time_stamp, dataTotal, 'b')

        self.canvas.draw()
