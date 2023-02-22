from data_manager import DataManager

# Class for getting TCP data with the given session
class TCP(DataManager):
  tags = ['tcpInSegs', 'tcpOutSegs', 'tcpInErrs', 'tcpRetransSegs',
          'tcpActiveOpens', 'tcpCurrEstab', 'tcpAttemptFails']
  headers = ['TCP Seg. In', 'TCP Seg. Out', 'TCP In Errors', 'TCP Seg. Retrans.',
             'TCP Active Opens', 'TCP Curr. Establ.', 'TCP Attempt Fails']

  def __init__(self, session):
    self.session = session
    super().__init__(session, TCP.tags)

