from data_manager import DataManager

# Class for getting TCP data with the given session
class TCP(DataManager):
  def __init__(self, session):
    self.session = session
    self.tags = ['tcpActiveOpens', 'tcpAttemptFails', 'tcpCurrEstab', 'tcpEstabResets',
                 'tcpMaxConn', 'tcpInErrs', 'tcpInSegs', 'tcpOutRsts', 'tcpOutSegs',
                 'tcpPassiveOpens', 'tcpRetransSegs', 'tcpRtoAlgorithm',
                 'tcpRtoMax', 'tcpRtoMin']
    super().__init__(session, self.tags)
