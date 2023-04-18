import sys
import random
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from scipy import stats

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
        self.lblGraphInstant = QLabel('Gráfico de consumo instantâneo:')
        self.lblGraphPerfil = QLabel('Gráfico de regressão linear em 6 tempos:')
        self.lblGraphPerfil2 = QLabel('Grafico de regressão linear cumulativo:')

        self.vbLayout.addWidget(self.lblGraphInstant)

        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)

        self.vbLayout.addWidget(self.canvas)
        self.vbLayout.addStretch(1)

        self.vbLayout.addWidget(self.lblGraphPerfil)

        self.perfil_canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.vbLayout.addWidget(self.perfil_canvas)

        self.vbLayout.addWidget(self.lblGraphPerfil2)
        self.perfil2_canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.vbLayout.addWidget(self.perfil2_canvas)


        self.firstTime = 0
        self.index = 0
        self.xdata = []
        self.dataModel = []


        self.setLayout(self.vbLayout)


    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        #self.zdata = self.zdata[1:] + [random.randint(0, 5)]

        frequency = 6

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

        if len(self.agent.data_map['ifInOctets']) > frequency:
            dataIA = []
            index = 0
            xdata = []

            if((len(self.agent.data_map['ifInOctets']) % frequency) == 0):
                for x in range(len(self.agent.data_map['ifInOctets']) - (frequency + 1), len(self.agent.data_map['ifInOctets'])):
                    dataIn = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                    dataOut = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                    data = dataIn + dataOut
                    time_diff = int(self.agent.data_map['ifInOctets'][x]['timestamp']) - int(self.agent.data_map['ifInOctets'][x-1]['timestamp'])
                    dataIA.append((1/(10*time_diff))*8*(data))
                    xdata.append(float(index))
                    index += 1
                
                # print('-----------------------')
                # print('x = ', xdata)                
                # print('y = ', dataIA)

                slope, intercept, r, p, std_err = stats.linregress(xdata, dataIA)
                
                # print('r = ', r)
                # print('p = ', p)
                # print('std_err = ', std_err)
                # print('-----------------------')

                def myfunc(x):
                    return slope * x + intercept

                mymodel = list(map(myfunc, xdata))
                
                if(self.firstTime == 0):
                    self.dataModel.append(mymodel[0])
                    self.dataModel.append(mymodel[len(mymodel) - 1])
                    self.firstTime = 1

                #print(len(mymodel))
                
                #Gráfico de consumo de perfil
                self.perfil_canvas.axes.cla()  # Clear the canvas.
                self.perfil_canvas.axes.yaxis.label.set_text('kbps')
                self.perfil_canvas.axes.grid(True, color='k', linestyle='-', linewidth=0.05)
                self.perfil_canvas.axes.plot(xdata, mymodel, dataIA, 'b')

                self.perfil_canvas.draw()

            else:
                self.firstTime = 0
                


        # print('size ---------------------------')
        # print(len(self.agent.data_map['ifInOctets']))
        # print('time ---------------------------')
        # print(time_stamp)
        # print('data ---------------------------')
        # print(dataTotal)
        #Gráfico de consumo instantâneo
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

        if(len(self.dataModel) > 2) :

            self.perfil2_canvas.axes.cla()
            x_perfil2 = []
            for x in range(len(self.dataModel)):
                x_perfil2.append(x)
            
            self.perfil2_canvas.axes.grid(True, color='k', linestyle='-', linewidth=0.05)
            self.perfil2_canvas.axes.plot(x_perfil2, self.dataModel, 'b')
            self.perfil2_canvas.draw()



        