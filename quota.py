from data_manager import DataManager

class QuotaMonitor(DataManager):
    tags = ['ifInOctets']
    headers = ['Entry Quota']

    def __init__(self, session):
        self.session = session
        super().__init__(session, QuotaMonitor.tags)