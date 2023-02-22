from tcp import TCP
from udp import UDP

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

    # gets udp and tcp data
    def get_data(self, session):
        if ( self.tcp is None ):
            self.tcp = TCP(session)

        if ( self.udp is None ):
            self.udp = UDP(session)

        data = {}
        try:
            data['tcp'] = self.tcp.get_data()
            data['udp'] = self.udp.get_data()
        except Exception as e:
            self.status = str(e)

        return data
