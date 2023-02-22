# define the agent class
class Agent():
    def __init__(self, ip, user, password, authProtocol, privacyProtocol):
        self.ip = ip
        self.user = user
        self.password = password
        self.authProtocol = authProtocol
        self.privacyProtocol = privacyProtocol
