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

        self.tags = [ 'udpInDatagrams', 'udpOutDatagrams', 'udpInErrors', 'tcpActiveOpens', 'tcpAttemptFails',
                      'tcpCurrEstab', 'tcpInErrs', 'tcpInSegs', 'tcpOutSegs', 'tcpRetransSegs' ]

        self.data = []

        for i in range(len(self.tags)):
            self.data.append([])
    
    def updateData(self, non_repeaters: int = 0, max_repetitions: int = 1):
        data = self.session.get_bulk(self.tags, non_repeaters, max_repetitions)
        for i in range(len(self.tags)):
            self.data[i].append({ 'tag': self.tags[i], 'time_stamp' : time.time(), 'data': data[i].value})
