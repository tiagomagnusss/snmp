from data_manager import DataManager

# Class for getting TCP data with the given session
class TCP(DataManager):
  def __init__(self, session):
    self.session = session
    self.tags = ['tcpActiveOpens', 'tcpAttemptFails', 'tcpCurrEstab', 'tcpEstabResets',
                 'tcpMaxConn', 'tcpInErrs', 'tcpOutRsts', 'tcpPassiveOpens']
    super().__init__(session, self.tags)
