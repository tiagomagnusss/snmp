from easysnmp import Session
from datetime import datetime  
import time

class User:

    def __init__(self, host, user, password, auth_protocol, privacy_protocol):

        self.session = Session(
            hostname = host, 
            security_level="auth_with_privacy", 
            security_username=user, 
            auth_password=password, 
            auth_protocol=auth_protocol, 
            privacy_password=password, 
            privacy_protocol=privacy_protocol, 
            version=3
            )
        
        self.tag_dic = { 'udpInDatagrams': 0, 'udpOutDatagrams': 1, 'udpInErrors': 2, 'tcpActiveOpens': 3, 'tcpAttemptFails': 4,
                           'tcpCurrEstab': 5, 'tcpInErrs': 6, 'tcpInSegs': 7, 'tcpOutSegs': 8, 'tcpRetransSegs':  9}

        self.tags = [ 'udpInDatagrams', 'udpOutDatagrams', 'udpInErrors', 'tcpActiveOpens', 'tcpAttemptFails',
                      'tcpCurrEstab', 'tcpInErrs', 'tcpInSegs', 'tcpOutSegs', 'tcpRetransSegs' ]

        self.data = []

        for i in range(len(self.tags)):
            self.data.append([])

    #busca todos os dados brutos
    def updateData(self, non_repeaters: int = 0, max_repetitions: int = 1):
        data = self.session.get_bulk(self.tags, non_repeaters, max_repetitions)
        for i in range(len(self.tags)):            
            self.data[i].append({ 'tag': self.tags[i], 'time_stamp' : time.time(), 'data': int(data[i].value)})
    
    def getTaxa(self, tag):
        lst = self.data[self.tag_dic[tag]]
        if(len(lst) > 1):
            print('taxa ',lst[len(lst)-1]['tag'], ': ', lst[len(lst)-1]['data'] - lst[len(lst)-2]['data'])
        else:
            print('0')
    
    def getDataInTime(self, time_start, time_end, tag):
        lst = self.data[self.tag_dic[tag]]

        if(len(lst) < 2):
            print('Quantidade insuficiente de dados')
            return 0

        if(time_end < lst[0]['time_stamp']):
            print('fora do intervalo')
            return 0
        
        if(time_start > lst[len(lst)-1]['time_stamp']):
            print('fora do intervalo')
            return 0
        
        i = 0

        while(time_start > lst[i]['time_stamp']):
            i += 1
        dataStart = lst[i]['data']

        i = len(lst) - 1
        while(time_end < lst[i]['time_stamp']):
            i -= 1
        dataEnd = lst[i]['data']
                
        print('--------------------\ndata: \n',dataStart,'\n', dataEnd,'\n--------------------')
        print(dataEnd-dataStart)
        pass       

