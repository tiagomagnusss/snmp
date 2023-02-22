from data_manager import DataManager

# Class for getting UDP data with the given session
class UDP(DataManager):
    tags = ['udpInDatagrams', 'udpOutDatagrams', 'udpInErrors']
    headers = ['UDP Datagrams In', 'UDP Datagrams Out', 'UDP Datagrams Errors']

    def __init__(self, session):
        self.session = session
        super().__init__(session, UDP.tags)
