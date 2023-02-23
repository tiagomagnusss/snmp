from tcp import TCP
from udp import UDP
from quota import QuotaMonitor

# define the agent class
class Agent():
    def __init__(self, ip, user, password, authProtocol, privacyProtocol, status = 'Connected'):
        self.ip = ip
        self.user = user
        self.password = password
        self.authProtocol = authProtocol
        self.privacyProtocol = privacyProtocol
        self.status = status

        self.tcp = None
        self.udp = None
        self.quota = None

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
        if ( self.tcp is None ):
            self.tcp = TCP(session)

        if ( self.udp is None ):
            self.udp = UDP(session)

        if ( self.quota is None ):
            self.quota = QuotaMonitor(session)

        data = {}
        if type(timestamp) is Agent:
            i = 1

        try:
            data['tcp'] = self.tcp.get_data(timestamp)
            data['udp'] = self.udp.get_data(timestamp)
            data['quota'] = self.quota.get_data(timestamp)

            if session.error_string != '' and data['tcp'] == {} and data['udp'] == {} and data['quota'] == {}:
                self.status = session.error_string
            else:
                self.status = 'Connected'
        except Exception as e:
            self.status = str(e)

        return data

