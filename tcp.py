from data_manager import DataManager

# Class for getting TCP data with the given session
class TCP(DataManager):
  tags = ['tcpActiveOpens', 'tcpAttemptFails', 'tcpCurrEstab', 'tcpEstabResets',
          'tcpMaxConn', 'tcpInErrs', 'tcpInSegs', 'tcpOutRsts', 'tcpOutSegs', 'tcpPassiveOpens']
  headers = ['TCP Active Opens', 'TCP Attempt Fails', 'TCP Curr. Established',
             'TCP Established Rst', 'TCP Max. Conn.', 'TCP In Errors',
             'TCP In Segs', 'TCP Out Rst', 'TCP Out Segs', 'TCP Passive Opens']

  def __init__(self, session):
    self.session = session
    super().__init__(session, TCP.tags)

