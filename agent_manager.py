from easysnmp import Session
import time

# handles multiple agents and update their data
class AgentManager():
    def __init__(self, agents = []):
        self.agent_map = {}
        self.session_map = {}

        for agent in agents:
            self.agent_map[agent.ip] = agent
            self.session_map[agent.ip] = self.create_session(agent)

        self.data = {}
        self.update_data()

    def add_agent(self, agent):
        if ( agent.ip in self.agent_map ):
            agent.status = 'Agent already exists'
            return False

        # try creating snmp session
        try:
            session = self.create_session(agent)

            if ( session is None ):
                return False

            self.agent_map[agent.ip] = agent
            self.session_map[agent.ip] = session
            self.update_data(agent)

            if (agent.status != 'Connected'):
                self.remove_agent(agent)
                return False

            return True
        except:
            return False

    def remove_agent(self, agent):
        if ( agent.ip not in self.agent_map ):
            return False

        del self.agent_map[agent.ip]
        del self.session_map[agent.ip]

    def create_session(self, agent):
        try:
            security_level = 'auth_with_privacy' if agent.privacyProtocol != 'None' else 'auth_without_privacy'
            privacy_protocol = agent.privacyProtocol if agent.privacyProtocol != 'None' else 'DEFAULT'
            privacy_password = agent.password if agent.privacyProtocol != 'None' else ''

            session = Session(
                hostname=agent.ip,
                version=3,
                security_level=security_level,
                security_username=agent.user,
                auth_protocol=agent.authProtocol,
                auth_password=agent.password,
                privacy_protocol=privacy_protocol,
                privacy_password=privacy_password
            )

            agent.session = session
            return session
        except Exception as e:
            #use exception message
            agent.status = str(e)
            return None

    def update_data(self, agent = None, timestamp = 0):
        if ( timestamp == 0 ):
            timestamp = int(time.time())

        if ( agent is None ):
            for agent in self.agent_map.values():
                self.update_data(agent, timestamp)
        else:
            data = agent.get_data(timestamp)
            self.data[agent.ip] = data

    def get_data(self):
        return self.data

