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
        self.lblRegressShort = QLabel('Gráfico de regressão linear em 15 segundos:')
        self.lblRegressTotal = QLabel('Grafico de regressão linear cumulativo:')
        self.lblRegressCompress = QLabel('Grafico comprimido:')

        self.vbLayout.addWidget(self.lblGraphInstant)
        
        self.canvas = MplCanvas(self, width=5, height=8, dpi=100)

        self.vbLayout.addWidget(self.canvas)
        self.vbLayout.addStretch(1)

        

        self.vbLayout.addWidget(self.lblRegressShort)

        self.regress_short_canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.vbLayout.addWidget(self.regress_short_canvas)

        self.vbLayout.addWidget(self.lblRegressTotal)
        self.regress_long_canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.vbLayout.addWidget(self.regress_long_canvas)

        self.vbLayout.addWidget(self.lblRegressCompress)
        self.regress_compress_canvas = MplCanvas(self, width=5, height=8, dpi=100)
        self.vbLayout.addWidget(self.regress_compress_canvas)

        self.setLayout(self.vbLayout)
        self.firstTime = 1
        self.compress = []


    def update_plot(self):

        times_short = 3
        times_long = 15

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

        if len(self.agent.data_map['ifInOctets']) > times_short:
            regress_short_data = []
            index = 0
            x_regress_short = []

            if((len(self.agent.data_map['ifInOctets']) % times_short) == 0):
                for x in range(len(self.agent.data_map['ifInOctets']) - (times_short + 1), len(self.agent.data_map['ifInOctets'])):
                    dataIn = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                    dataOut = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                    data = dataIn + dataOut
                    time_diff = int(self.agent.data_map['ifInOctets'][x]['timestamp']) - int(self.agent.data_map['ifInOctets'][x-1]['timestamp'])
                    regress_short_data.append((1/(10*time_diff))*8*(data))
                    x_regress_short.append(float(index))
                    index += 1

                slope, intercept, r, p, std_err = stats.linregress(x_regress_short, regress_short_data)
                
                def regressFun(x):
                    return slope * x + intercept

                short_regress_model = list(map(regressFun, x_regress_short))

                for x in range(len(x_regress_short)):
                    x_regress_short[x] = -15 + x_regress_short[x]*5
                
                #Gráfico de consumo dos ultimos times_short*5s segundos
                self.regress_short_canvas.axes.cla()  # Clear the canvas.                
                self.regress_short_canvas.axes.yaxis.label.set_text('kbps')
                self.regress_short_canvas.axes.grid(True, color='k', linestyle='-', linewidth=0.05)
                self.regress_short_canvas.axes.plot(x_regress_short, short_regress_model, 'r')                
                #self.regress_short_canvas.axes.plot(x_regress_short, regress_short_data, 'b')
                self.regress_short_canvas.draw()

        if len(self.agent.data_map['ifInOctets']) > times_long:
            regress_long_data = []
            index = 0
            x_regress_long = []

            if((len(self.agent.data_map['ifInOctets']) % times_long) == 0):
                for x in range(len(self.agent.data_map['ifInOctets']) - (times_long + 1), len(self.agent.data_map['ifInOctets'])):
                    dataIn = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                    dataOut = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                    data = dataIn + dataOut
                    time_diff = int(self.agent.data_map['ifInOctets'][x]['timestamp']) - int(self.agent.data_map['ifInOctets'][x-1]['timestamp'])
                    regress_long_data.append((1/(10*time_diff))*8*(data))
                    x_regress_long.append(float(index))
                    index += 1

                slope, intercept, r, p, std_err = stats.linregress(x_regress_long, regress_long_data)
                
                def regressFun(x):
                    return slope * x + intercept

                long_regress_model = list(map(regressFun, x_regress_long))

                
                if self.firstTime == 1 :
                    self.compress.append(long_regress_model[0])
                    self.compress.append(long_regress_model[len(long_regress_model) - 1])
                    self.firstTime = 0

                if len(self.compress) > 2:
                    x_long_canvas = []
                    for x in range(len(self.compress)):
                        x_long_canvas.append(x)
                
                    #Gráfico de consumo dos ultimos times_long*5s segundos
                    self.regress_compress_canvas.axes.cla()  # Clear the canvas.                
                    self.regress_compress_canvas.axes.yaxis.label.set_text('kbps')
                    self.regress_compress_canvas.axes.grid(True, color='k', linestyle='-', linewidth=0.05)
                    self.regress_compress_canvas.axes.plot(x_long_canvas, self.compress, 'b')                
                    #self.regress_compress_canvas.axes.plot(x_regress_long, regress_long_data, 'b')
                    self.regress_compress_canvas.draw()
                
            else:
                self.firstTime = 1

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

        #Faz a regressão para todos os dados
        if(len(self.agent.data_map['ifInOctets']) > 2) :            

            self.regress_long_canvas.axes.cla()
            x_perfil2 = []
            y_perfil2 = []
            for x in range(len(self.agent.data_map['ifInOctets'])):
                x_perfil2.append(x)
                dataIn = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                dataOut = int(self.agent.data_map['ifInOctets'][x]['value']) - int(self.agent.data_map['ifInOctets'][x-1]['value'])
                data = dataIn + dataOut
                time_diff = int(self.agent.data_map['ifInOctets'][x]['timestamp']) - int(self.agent.data_map['ifInOctets'][x-1]['timestamp'])
                y_perfil2.append((1/(10*time_diff))*8*(data))
            
            slope, intercept, r, p, std_err = stats.linregress(x_perfil2, y_perfil2)

            def myfunc(x):
                    return slope * x + intercept

            mymodel = list(map(myfunc, x_perfil2))
                        
            self.regress_long_canvas.axes.grid(True, color='k', linestyle='-', linewidth=0.05)
            self.regress_long_canvas.axes.plot(x_perfil2, mymodel, 'g')
            self.regress_long_canvas.axes.yaxis.label.set_text('kbps')
            # self.regress_long_canvas.axes.plot(x_perfil2, y_perfil2, 'b')
            self.regress_long_canvas.draw()



        