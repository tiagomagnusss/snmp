from data_manager import DataManager

# Class for getting UDP data with the given session
class UDP(DataManager):
    tags = ['udpInDatagrams', 'udpOutDatagrams', 'udpInErrors']
    headers = ['UDP In', 'UDP Out', 'UDP Errors']

    def __init__(self, session):
        self.session = session
        super().__init__(session, UDP.tags)
