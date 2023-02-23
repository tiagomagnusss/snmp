from tcp import TCP
from udp import UDP
from quota import QuotaMonitor
from data_manager import DataManager

# define the agent class
class Agent():
    def __init__(self, ip, user, password, authProtocol, privacyProtocol, status = 'Connected'):
        self.ip = ip
        self.user = user
        self.password = password
        self.authProtocol = authProtocol
        self.privacyProtocol = privacyProtocol
        self.status = status

        self.data_manager = None

    def __dict__(self):
        return {
            'ip': self.ip,
            'user': self.user,
            'password': self.password,
            'authProtocol': self.authProtocol,
            'privacyProtocol': self.privacyProtocol
        }

    # gets udp and tcp data
    def get_data(self, session, timestamp):
        if ( self.data_manager is None ):
            self.data_manager = DataManager(session, TCP.tags + UDP.tags + QuotaMonitor.tags)

        data = {}
        try:
            data = self.data_manager.get_data(timestamp)

            if session.error_string != '' and data == {}:
                self.status = session.error_string
            else:
                self.status = 'Connected'
        except Exception as e:
            self.status = str(e)

        return data

