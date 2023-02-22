from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QComboBox, QRadioButton, QLabel, QAction, QFormLayout, QHBoxLayout, QVBoxLayout, QTableWidget, QTableView, QTableWidgetItem, QPushButton, QLineEdit
from PyQt5.QtCore import pyqtSlot, Qt, QRegExp
from PyQt5.QtGui import QPalette, QIcon, QColor, QRegExpValidator
from agent import Agent

import pickle
import sys
import os

class NumericTableWidgetItem(QTableWidgetItem):
    def __init__(self, number):
        QTableWidgetItem.__init__(self, number, QTableWidgetItem.UserType)
        self.__number = number

    def __lt__(self, other):
        return int(self.__number) < int(other.__number)

class mainGUI(QWidget):
    def __init__(self):
        super().__init__()
        # self.setWindowIcon(QIcon(os.path.dirname(__file__) + "/" + "randomico.ico"))
        self.title = 'SNMPv3 counter'
        self.left = 0
        self.top = 0
        self.width = 1280
        self.height = 700
        # self.root = root
        # self.courses = courses
        # self.periods = periods
        # self.filtered = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.vbLayout = QVBoxLayout()
        self.createAddressBar()
        self.createView()
        # self.createView()

        # Define o layout da tela
        self.setLayout(self.vbLayout)

        # e mostra a janela
        self.showMaximized()

    def createAddressBar(self):
        """ Cria o hbox superior da tela """
        self.hbAddress = QHBoxLayout()

        # ip with a mask
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)

        self.txtIp = QLineEdit(self)
        self.txtIp.setValidator(ipValidator)

        self.txtUser = QLineEdit(self)
        self.txtPassword = QLineEdit(self)
        self.txtAuthProtocol = QLineEdit(self)
        self.txtPrivacyProtocol = QLineEdit(self)

        self.cbAuthProtocol = QComboBox(self)
        self.cbAuthProtocol.setEditable(True)
        self.cbAuthProtocol.setAutoFillBackground(True)
        self.cbAuthProtocol.addItems(['None', 'MD5', 'SHA'])

        self.cbPrivacyProtocol = QComboBox(self)
        self.cbPrivacyProtocol.setEditable(True)
        self.cbPrivacyProtocol.setAutoFillBackground(True)
        self.cbPrivacyProtocol.addItems(['None', 'DES', 'AES'])

        self.btnAdd = QPushButton('Add agent', self)
        self.btnAdd.clicked.connect(self.on_add)

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

        # coloca na tela
        self.vbLayout.addLayout(self.hbAddress)

    def createView(self):
        """ Cria a tabela de agentes """
        # cria a tabela
        self.tblAgents = QTableWidget(self)
        self.tblAgents.setRowCount(0)
        self.tblAgents.setColumnCount(6)
        self.tblAgents.setHorizontalHeaderLabels(['IP', 'User', 'Password', 'Auth Protocol', 'Privacy Protocol', 'Actions'])

        # carrega os agentes
        self.agents = self.loadAgents()

        # adiciona os agentes na tabela
        for agent in self.agents:
            self.addAgentToTable(agent)

        # coloca na tela
        self.vbLayout.addWidget(self.tblAgents)

    def loadAgents(self):
        """ Carrega os agentes salvos """
        return []
        try:
            with open('agents.pickle', 'rb') as handle:
                return pickle.load(handle)
        except:
            return []

    def saveAgents(self):
        """ Salva os agentes """
        return
        with open('agents.pickle', 'wb') as handle:
            pickle.dump(self.agents, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def addAgentToTable(self, agent):
        """ Adiciona um agente na tabela """
        # pega o numero de linhas
        rowPosition = self.tblAgents.rowCount()

        # adiciona uma linha
        self.tblAgents.insertRow(rowPosition)

        # adiciona os dados
        self.tblAgents.setItem(rowPosition, 0, QTableWidgetItem(agent.ip))
        self.tblAgents.setItem(rowPosition, 1, QTableWidgetItem(agent.user))
        self.tblAgents.setItem(rowPosition, 2, QTableWidgetItem(agent.password))
        self.tblAgents.setItem(rowPosition, 3, QTableWidgetItem(agent.authProtocol))
        self.tblAgents.setItem(rowPosition, 4, QTableWidgetItem(agent.privacyProtocol))

        # adiciona o botao de remover
        btnRemove = QPushButton('Remove', self)
        btnRemove.clicked.connect(self.on_remove)
        self.tblAgents.setCellWidget(rowPosition, 5, btnRemove)

    @pyqtSlot()
    def on_remove(self):
        """ Remove um agente """
        # pega o botao que foi clicado
        button = self.sender()

        # get row of button
        row = self.tblAgents.indexAt(button.pos()).row()

        # remove o agente da lista
        self.agents.pop(row)

        # salva os agentes
        self.saveAgents()

        # remove a linha da tabela
        self.tblAgents.removeRow(row)

    @pyqtSlot()
    def on_add(self):
        """ Adiciona um agente """
        # pega os dados do agente
        ip = self.txtIp.text()
        user = self.txtUser.text()
        password = self.txtPassword.text()
        authProtocol = self.cbAuthProtocol.currentText()
        privacyProtocol = self.cbPrivacyProtocol.currentText()

        # verifica se os campos estao vazios
        if ip == '' or user == '' or password == '' or authProtocol == '' or privacyProtocol == '':
            QMessageBox.about(self, 'Error', 'All fields are required')
            return

        # print all information on a warning box
        # QMessageBox.about(self, 'Warning', 'IP: ' + ip + '
        QMessageBox.warning(self, 'Warning', f"IP: {ip} User: {user} Password: {password} Auth Protocol: {authProtocol} Privacy Protocol: {privacyProtocol}")

        # cria o agente
        agent = Agent(ip, user, password, authProtocol, privacyProtocol)

        # adiciona o agente na lista
        self.agents.append(agent)

        # salva os agentes
        self.saveAgents()

        # adiciona o agente na tabela
        self.addAgentToTable(agent)

        self.txtIp.clear()
        self.txtUser.clear()
        self.txtPassword.clear()
        self.cbAuthProtocol.setCurrentIndex(0)
        self.cbPrivacyProtocol.setCurrentIndex(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    palette = QPalette()
    palette.setColor(QPalette.Background, QColor(110, 110, 110, 230))
    app.setPalette(palette)

    ex = mainGUI()
    sys.exit(app.exec_())