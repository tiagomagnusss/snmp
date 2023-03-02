from collections import OrderedDict
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QMessageBox, QComboBox, QLabel, QHBoxLayout, QVBoxLayout, QTableWidget, QTableView, QTableWidgetItem, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSlot, QRegExp, QTimer, Qt
from PyQt5.QtGui import QPalette, QIcon, QColor, QRegExpValidator, QIntValidator, QPixmap, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from agent import Agent
from agent_manager import AgentManager
from stats_window import StatsWindow
from datetime import datetime
import pickle
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime

class mainGUI(QWidget):
    status = "STATUS: "

    def __init__(self):
        super().__init__()
        # self.setWindowIcon(QIcon(os.path.dirname(__file__) + "/" + "randomico.ico"))
        self.title = 'SNMPv3 counter'
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 700
        self.agents = []
        self.agent_manager = AgentManager()
        self.quotaTags = ['ifInOctets']
        self.faultTags = ['ifOperStatus', 'ifAdminStatus']
        self.defaultHeaders = ['Status', 'IP', 'User', 'Device', 'Privacy Protocol']
        self.performanceHeaders = ['Input Traffic', 'Output Traffic', 'Interface usage', 'Entry Quota']
        self.headerCount = len(self.defaultHeaders) + len(self.performanceHeaders)
        self.statusBar = QLabel(f"{mainGUI.status} Ready")
        self.quota_user = 0
        self.stats = StatsWindow(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.vbLayout = QVBoxLayout()

        self.createAddressBar()
        self.createTasksBox()
        self.createView()
        self.createStatusBar()

        # Define o layout da tela
        self.setLayout(self.vbLayout)

        # e mostra a janela
        self.showMaximized()

    def createAddressBar(self):
        """ Cria o hbox superior da tela """
        self.hbAddress = QHBoxLayout()

        self.createInterval(self.hbAddress)

        # ip with a mask
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)

        self.txtIp = QLineEdit(self, placeholderText='IP address')
        self.txtIp.setValidator(ipValidator)

        self.txtUser = QLineEdit(self, placeholderText='Username')
        self.txtPassword = QLineEdit(self, placeholderText='Password')

        self.cbAuthProtocol = QComboBox(self)
        self.cbAuthProtocol.setEditable(False)
        self.cbAuthProtocol.setAutoFillBackground(True)
        self.cbAuthProtocol.addItems(['MD5', 'SHA'])

        self.cbPrivacyProtocol = QComboBox(self)
        self.cbPrivacyProtocol.setEditable(False)
        self.cbPrivacyProtocol.setAutoFillBackground(True)
        self.cbPrivacyProtocol.addItems(['None', 'DES', 'AES'])

        self.btnAdd = QPushButton('Add agent', self)
        self.btnAdd.clicked.connect(self.on_add)

        self.btnSave = QPushButton('Save', self)
        self.btnSave.clicked.connect(self.on_save)

        self.btnLoad = QPushButton('Load', self)
        self.btnLoad.clicked.connect(self.on_load)

        # create line with address, ip, user, password, auth, privacy protocol and add button
        self.hbAddress.addWidget(QLabel('IP address: '))
        self.hbAddress.addWidget(self.txtIp)
        self.hbAddress.addWidget(QLabel('User: '))
        self.hbAddress.addWidget(self.txtUser)
        self.hbAddress.addWidget(QLabel('Password: '))
        self.hbAddress.addWidget(self.txtPassword)
        self.hbAddress.addWidget(QLabel('Auth Protocol: '))
        self.hbAddress.addWidget(self.cbAuthProtocol)
        self.hbAddress.addWidget(QLabel('Privacy Protocol: '))
        self.hbAddress.addWidget(self.cbPrivacyProtocol)
        self.hbAddress.addWidget(self.btnAdd)

        self.hbAddress.addWidget(QLabel(''))
        self.hbAddress.addWidget(QLabel(''))
        self.hbAddress.addWidget(QLabel(''))
        self.hbAddress.addWidget(QLabel(''))
        self.hbAddress.addWidget(self.btnSave)
        self.hbAddress.addWidget(self.btnLoad)

        # coloca na tela
        self.vbLayout.addLayout(self.hbAddress)

    def createInterval(self, hbAddress):
        self.hbInterval = QHBoxLayout()

        self.lblRate = QLabel('Interval (seconds): ')
        self.cbRate = QComboBox(self)
        self.cbRate.setEditable(True)
        self.cbRate.setAutoFillBackground(True)
        self.cbRate.addItems(['1', '2', '5', '10', '20', '50'])
        self.cbRate.setCurrentIndex(2)
        self.cbRate.setEditable(False)
        self.cbRate.currentTextChanged.connect(self.on_interval_changed)

        self.hbInterval.addWidget(self.lblRate)
        self.hbInterval.addWidget(self.cbRate)

        hbAddress.addLayout(self.hbInterval)
        hbAddress.addWidget(QLabel(''))
        hbAddress.addWidget(QLabel(''))
        hbAddress.addWidget(QLabel(''))

    def createView(self):
        """ Cria a tabela de agentes """
        # cria a tabela
        self.tblAgents = QTableWidget(self)
        self.tblAgents.setRowCount(0)
        self.tblAgents.setSelectionBehavior(QTableView.SelectRows)
        self.tblAgents.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tblAgents.setAlternatingRowColors(True)

        self.tblAgents.setColumnCount(self.headerCount + 2)
        self.tblAgents.setHorizontalHeaderLabels(self.defaultHeaders + self.performanceHeaders + ['Analyze', 'Actions'])

        self.tblAgents.resizeColumnsToContents()

        # coloca na tela
        self.vbLayout.addWidget(self.tblAgents)

        self.timer = QTimer()
        self.timer.setInterval(5000)
        self.timer.timeout.connect(self.on_timer)

        # carrega os agentes
        self.loadAgents()

    def createStatusBar(self):
        """ Cria a barra de status """
        # texto de log no fim da tela
        self.vbLayout.addWidget(self.statusBar)

    def createTasksBox(self):
        self.hbQuota = QHBoxLayout()
        self.vbLayout.addLayout(self.hbQuota, stretch=0)

        self.btnShowQuotasCharts = QPushButton("Show Quotas", self)
        self.btnShowFaultCharts = QPushButton("Show Fault", self)
        self.txtQuota = QLineEdit(self, placeholderText='Enter Quota Value (MB)')
        self.txtQuota.setValidator(QIntValidator())
        self.txtQuota.setText(str(self.quota_user))
        self.hbQuota.addWidget(QLabel('Quota Value (MB): '), alignment=Qt.AlignLeft)
        self.hbQuota.addWidget(self.txtQuota, alignment=Qt.AlignLeft)
        self.hbQuota.addWidget(self.btnShowQuotasCharts, alignment=Qt.AlignLeft)
        self.hbQuota.addWidget(self.btnShowFaultCharts, alignment=Qt.AlignLeft)
        self.hbQuota.addStretch()

        # self.hbQuota.setAlignment(Qt.AlignLeft)

        self.btnShowQuotasCharts.clicked.connect(self.showQuotaCharts)
        self.btnShowFaultCharts.clicked.connect(self.showFaultCharts)
        self.txtQuota.textChanged.connect(self.on_quota_changed)

    def setStatus(self, status):
        """ Atualiza o texto de status """
        self.statusBar.setText(f"{mainGUI.status} {status}")

    def loadAgents(self):
        """ Carrega os agentes salvos """
        try:
            with open('agents.pickle', 'rb') as handle:
                agent_details = pickle.load(handle)
                for agent_detail in agent_details:
                    agent = Agent(**agent_detail)
                    self.on_add(agent)
        except Exception as e:
            self.setStatus(f"Error while loading agents. {str(e)}")
            return []

    def saveAgents(self):
        """ Salva os agentes """
        try:
            with open('agents.pickle', 'wb') as handle:
                agent_details = []
                for agent in self.agents:
                    agent_details.append(agent.__dict__())

                pickle.dump(agent_details, handle, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            self.setStatus(f"Error while saving agents. {str(e)}")

    def setData(self, agent, rowPosition):
        agentData = self.agent_manager.get_data()[agent.ip]

        if agentData is None or agentData == {}:
            self.tblAgents.setItem(rowPosition, 0, QTableWidgetItem(agent.status))
            self.setStatus(f"Error while fetching data for agent {agent.ip}")
            return

        statusWidget = QTableWidgetItem(agent.status)
        statusIcon = 'network-transmit' if agent.status == 'Connected' else 'network-error'
        statusWidget.setIcon(QIcon.fromTheme(statusIcon))
        self.tblAgents.setItem(rowPosition, 0, statusWidget)
        self.tblAgents.setItem(rowPosition, 1, QTableWidgetItem(agent.ip))
        self.tblAgents.setItem(rowPosition, 2, QTableWidgetItem(agent.user))
        self.tblAgents.setItem(rowPosition, 3, QTableWidgetItem(agentData["sysName"]))
        self.tblAgents.setItem(rowPosition, 4, QTableWidgetItem(agent.privacyProtocol))

        for index, item in enumerate(agent.outputTags):
            if item == 'ifInOctets':
                self.tblAgents.setItem(rowPosition, index + 5, self.quotaCell(agentData[item]))
            elif not (item == 'ifOperStatus' or item == 'ifAdminStatus' or item == 'ifLastChange'):
                self.tblAgents.setItem(rowPosition, index + 5, QTableWidgetItem(agentData[item]))

    def quotaCell(self, usage):
        if self.quota_user != '':
            if int(self.quota_user) > 0:
                pct_quota = round(((int(usage)/1000000)/int(self.quota_user))*100,2)

                if pct_quota >= 90 and pct_quota <=100:
                    cellExceeded = QTableWidgetItem(str(pct_quota) + '%')
                    cellExceeded.setIcon(QIcon.fromTheme('dialog-warning'))
                if pct_quota >= 100:
                    cellExceeded = QTableWidgetItem('> 100%')
                    cellExceeded.setIcon(QIcon.fromTheme('dialog-warning'))
                else:
                    cellExceeded = QTableWidgetItem(str(pct_quota) + '%')
                    cellExceeded.setIcon(QIcon.fromTheme('dialog-ok-apply'))
            else:
                cellExceeded = QTableWidgetItem()
                cellExceeded.setIcon(QIcon.fromTheme('dialog-warning'))
        else:
            cellExceeded = QTableWidgetItem()
            cellExceeded.setIcon(QIcon.fromTheme('dialog-warning'))

        return cellExceeded

    def updateTable(self):
        """ Atualiza a tabela de agentes """
        # atualiza os agentes
        for rowPosition, agent in enumerate(self.agents):
            self.setData(agent, rowPosition)

        self.tblAgents.resizeColumnsToContents()
        tick = datetime.now().strftime('%H:%M:%S')
        self.setStatus(f"Updated {len(self.agents)} agents at {tick}")

    def addAgentToTable(self, agent):
        """ Adiciona um agente na tabela """
        # pega o numero de linhas
        rowPosition = self.tblAgents.rowCount()

        # adiciona uma linha
        self.tblAgents.insertRow(rowPosition)
        self.setData(agent, rowPosition)

        # adiciona o botao de analise
        btnAnalyze = QPushButton('Analyze', self)
        btnAnalyze.clicked.connect(self.on_analyze)
        btnAnalyze.setIcon(QIcon.fromTheme("system-search"))
        self.tblAgents.setCellWidget(rowPosition, self.tblAgents.columnCount() - 2, btnAnalyze)
        self.tblAgents.resizeColumnsToContents()

        # adiciona o botao de remover
        btnRemove = QPushButton('Remove', self)
        btnRemove.clicked.connect(self.on_remove)
        btnRemove.setIcon(QIcon.fromTheme("edit-delete"))
        self.tblAgents.setCellWidget(rowPosition, self.tblAgents.columnCount() - 1, btnRemove)
        self.tblAgents.resizeColumnsToContents()

        if not self.timer.isActive():
            self.timer.start()

    @pyqtSlot()
    def on_quota_changed(self):
        self.quota_user = self.txtQuota.text()
        self.setStatus(f"Quota changed to {self.quota_user} MB")

    @pyqtSlot()
    def on_interval_changed(self):
        """ Altera o intervalo de atualizacao """
        self.timer.setInterval(int(self.cbRate.currentText()) * 1000)
        self.setStatus(f"Interval changed to {self.cbRate.currentText()} seconds")

    @pyqtSlot()
    def on_timer(self):
        """ Atualiza os dados dos agentes """
        self.agent_manager.update_data()
        self.updateTable()

    @pyqtSlot()
    def on_remove(self):
        """ Remove um agente """
        # pega o botao que foi clicado
        button = self.sender()

        # get row of button
        row = self.tblAgents.indexAt(button.pos()).row()

        ip = self.tblAgents.item(row, 1).text()
        self.agent_manager.remove_agent(self.agents[row])

        # remove o agente da lista
        self.agents.pop(row)

        # salva os agentes
        self.saveAgents()

        # remove a linha da tabela
        self.tblAgents.removeRow(row)

        if len(self.agents) == 0:
            self.timer.stop()

        self.setStatus(f"Removed agent {ip}")

    @pyqtSlot()
    def on_analyze(self):
        # open stats window
        button = self.sender()
        row = self.tblAgents.indexAt(button.pos()).row()
        ip = self.tblAgents.item(row, 1).text()
        self.stats.showFor(ip)

    @pyqtSlot()
    def on_add(self, new_agent = None):
        """ Adiciona um agente """
        if new_agent is None:
            ip = self.txtIp.text()
            user = self.txtUser.text()
            password = self.txtPassword.text()
            authProtocol = self.cbAuthProtocol.currentText()
            privacyProtocol = self.cbPrivacyProtocol.currentText()
        else:
            ip = new_agent.ip
            user = new_agent.user
            password = new_agent.password
            authProtocol = new_agent.authProtocol
            privacyProtocol = new_agent.privacyProtocol

        errors = []
        # verifica se os campos estao vazios
        if ip == '':
            errors.append('IP is required')
        elif user == '':
            errors.append('User is required')
        elif privacyProtocol != 'None' and password == '':
            errors.append('Password is required if privacy protocol is set')

        if len(errors) > 0:
            QMessageBox.warning(self, 'Error', '. '.join(errors))
            self.setStatus(f"Error adding agent {ip}. {'. '.join(errors)}")
            return

        if new_agent is None:
            # cria o agente
            agent = Agent(ip, user, password, authProtocol, privacyProtocol, {})
        else:
            agent = new_agent

        # inicia a conexão
        result = self.agent_manager.add_agent(agent)

        if result == False:
            QMessageBox.critical(self, 'Error', f"Error adding agent: {agent.status}")
            self.setStatus(f"Error adding agent {ip}. {agent.status}")
            del agent
            return
        elif new_agent is None:
            QMessageBox.information(self, 'Success', 'Agent added successfully')

        # adiciona o agente na lista
        self.agents.append(agent)

        # salva os agentes
        self.saveAgents()

        # adiciona o agente na tabela
        self.addAgentToTable(agent)
        self.setStatus(f"Agent {agent.ip} added successfully")

    @pyqtSlot()
    def on_save(self):
        """ Salva os agentes """
        self.saveAgents()
        self.setStatus('Agents saved successfully')

    @pyqtSlot()
    def on_load(self):
        """ Carrega os agentes """
        self.loadAgents()

    @pyqtSlot()
    def on_close(self):
        """ Fecha o programa """
        self.saveAgents()
        app.quit()

    def showQuotaCharts(self):
        """ Mostra os gráficos de pizza com os dados de quota """

         # Cria uma nova janela
        self.allChartsWindow = QDialog(self)
        self.allChartsWindow.setWindowTitle("Quota Monitoring")

        # Cria um layout horizontal para a nova janela
        hbox = QHBoxLayout(self.allChartsWindow)

        for agent in self.agents:
            agentData = self.agent_manager.get_data()[agent.ip]
            if agentData is None or agentData == {}:
                continue

            for item in self.quotaTags:
                fig, ax = plt.subplots()

                if self.quota_user != '':
                    if int(self.quota_user) > 0:
                        if (int(agentData[item])/1000000)<= int(self.quota_user):
                            quota_values = [int(self.quota_user)-(int(agentData[item])/1000000), (int(agentData[item])/1000000)]
                            quota_labels = ['Quota Disponível', 'Quota Utilizada']
                            ax.pie(quota_values, labels=quota_labels, autopct=lambda pct: f'{pct:.2f}%\n({pct/100*sum(quota_values):.2f})', startangle=90, colors=['green', 'blue'])
                        else:
                            quota_values = [(int(agentData[item])/1000000)-int(self.quota_user), int(self.quota_user)]
                            quota_labels = ['Quota Excedente', 'Quota Determinada']
                            ax.pie(quota_values, labels=quota_labels, autopct=lambda pct: f'{pct:.2f}%\n({pct/100*sum(quota_values):.2f})', startangle=90, colors=['red', 'blue'])
                    else:
                        quota_values = [int(self.quota_user), (int(agentData[item])/1000000)]
                        quota_labels = ['Quota Disponível', 'Quota Utilizada']
                        ax.pie(quota_values, labels=quota_labels, autopct=lambda pct: f'{pct:.2f}%\n({pct/100*sum(quota_values):.2f})', startangle=90, colors=['green', 'blue'])
                else:
                    quota_values = [int(self.quota_user), (int(agentData[item])/1000000)]
                    quota_labels = ['Quota Disponível', 'Quota Utilizada']
                    ax.pie(quota_values, labels=quota_labels, autopct=lambda pct: f'{pct:.2f}%\n({pct/100*sum(quota_values):.2f})', startangle=90, colors=['green', 'blue'])

                ax.axis('equal')
                ax.set_title(f"Quota (MB) for agent {agent.user} - {agent.ip}")

                chartLabel = QLabel(self.allChartsWindow)
                chartLabel.setPixmap(QPixmap.fromImage(self.matplotlibToQImage(fig)))
                chartLabel.setMinimumSize(400, 300)

                hbox.addWidget(chartLabel)

        self.allChartsWindow.show()

    def getFaultData(self):

        data_oper = []
        data_admin = []

        for agent in self.agents:
            for tag in self.faultTags:
                for item in agent.data_map[tag]:
                    item_chart = item.copy()

                    if item['value'] == '1':
                        item_chart['value'] = '0'
                        item_chart['agent'] = agent.user
                        item_chart['ip'] = agent.ip
                    else:
                        item_chart['value'] = '1'
                        item_chart['agent'] = agent.user
                        item_chart['ip'] = agent.ip

                    if tag == 'ifOperStatus':
                        data_oper.append(item_chart)
                    else:
                        data_admin.append(item_chart)


        # Crie um dicionário para armazenar os dados
        data = {}

        # Itere sobre cada dicionário em data_oper e data_admin
        for item in data_oper + data_admin:
            # Crie a chave do dicionário usando a combinação de timestamp, agent e ip
            key = (item['timestamp'], item['agent'], item['ip'])
            # Verifique se a chave existe no dicionário
            if key in data:
                # Se o valor do dicionário existente for '1', mantenha o dicionário existente
                if data[key]['value'] == '1':
                    continue
                # Se o valor do dicionário atual for '1', atualize a chave com o valor atual do dicionário
                if item['value'] == '1':
                    data[key] = item
                # Caso contrário, mantenha o primeiro dicionário encontrado com valor '0'
                else:
                    continue
            # Se a chave não existir, adicione a chave com o valor atual do dicionário
            else:
                data[key] = item

        # Converta o dicionário resultante em uma lista de dicionários
        data_list = list(data.values())

        ips = [item['ip'] for item in data_list]
        ips = list(OrderedDict.fromkeys(ips))

        return data_list, ips

    def showFaultCharts(self):
        # Cria uma nova janela
        self.allChartsWindow = QDialog(self)
        self.allChartsWindow.setWindowTitle("Fault Monitoring")

        # Cria um layout horizontal para a nova janela
        hbox = QHBoxLayout(self.allChartsWindow)

        data_list, allIps = self.getFaultData()

        # criar a figura e os eixos do gráfico
        fig, ax = plt.subplots(figsize=(12,6), dpi=100)

        # definir o formato de data para o eixo x
        date_fmt = mdates.DateFormatter('%Y-%m-%d %H:%M:%S')
        ax.xaxis.set_major_formatter(date_fmt)
        
        for ip in allIps:
            timestamps = []
            values = []
            for item in data_list:
                if item['ip'] == ip:
                    # converter o timestamp em datetime
                    timestamps.append(datetime.fromtimestamp(int(item['timestamp'])))

                    # extrair os valores de 'value' para cada lista
                    values.append(int(item['value']) )

            # plotar as linhas
            ax.plot(timestamps, values, label=ip)

        # adicionar o título e as legendas
        ax.set_title('Status da Interface')
        ax.set_xlabel('Tempo')
        ax.set_ylabel('Falha')
        ax.set_ylim(0, 2)
        hours = mdates.HourLocator(interval=1)
        ax.xaxis.set_major_locator(hours)
        ax.legend()

        chartLabel = QLabel(self.allChartsWindow)
        chartLabel.setPixmap(QPixmap.fromImage(self.matplotlibToQImage(fig)))
        chartLabel.setMinimumSize(400, 300)

        hbox.addWidget(chartLabel)

        self.allChartsWindow.show()         

    def matplotlibToQImage(self, figure):
        canvas = FigureCanvas(figure)
        canvas.draw()

        size = canvas.size()
        width, height = size.width(), size.height()

        image = QImage(canvas.buffer_rgba(), width, height, QImage.Format_RGBA8888)

        return image

if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Background, QColor(230, 230, 230, 140))
    app.setPalette(palette)

    app.setQuitOnLastWindowClosed(False)
    ex = mainGUI()
    app.lastWindowClosed.connect(ex.on_close)

    sys.exit(app.exec_())