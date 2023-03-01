# define the agent class
class Agent():
    def __init__(self, ip, user, password, authProtocol, privacyProtocol, data_map = {}, status = 'Connected'):
        self.ip = ip
        self.user = user
        self.password = password
        self.authProtocol = authProtocol
        self.privacyProtocol = privacyProtocol
        self.status = status
        self.session = None
        self.data_map = data_map

        self.tags = ['sysName', 'ifInOctets', 'ifOutOctets', 'ifSpeed', 'ifOperStatus', 'ifAdminStatus']
        self.outputTags = ['inBandwidth', 'outBandwidth', 'ifBandwidth', 'ifInOctets']

    def __dict__(self):
        return {
            'ip': self.ip,
            'user': self.user,
            'password': self.password,
            'authProtocol': self.authProtocol,
            'privacyProtocol': self.privacyProtocol,
            'status': self.status,
            'data_map': self.data_map,
        }

    def get_data(self, timestamp: int, non_repeaters: int = 0, max_repetitions: int = 1) -> dict:
        if ( len(self.tags) == 0 ):
            return {}

        # ignore if timestamp is the same as the last
        try:
            data = self.session.get_bulk(self.tags, non_repeaters, max_repetitions)

            if self.session.error_string != '' and data == {}:
                self.status = self.session.error_string
                self.session.error_string = ''
                return {}
            else:
                self.status = 'Connected'

            for item in data:
                # if ( item.snmp_type in ('COUNTER', 'GAUGE', 'INTEGER') ):
                if ( item.oid not in self.data_map ):
                    self.data_map[item.oid] = []

                self.data_map[item.oid].append({ "timestamp": timestamp, "value": item.value })
        except Exception as e:
            self.status = str(e)

        self.process_data()
        return self.generate_output()

    def generate_output(self):
        new_data_map = {}

        for tag in self.outputTags + self.tags:
            if tag not in self.data_map:
                continue

            if isinstance(self.data_map[tag], list):
                new_data_map[tag] = self.data_map[tag][-1]['value']
            else:
                new_data_map[tag] = self.data_map[tag]

        return new_data_map

    def process_data(self):
        if 'ifInOctets' in self.data_map and 'ifOutOctets' in self.data_map and 'ifSpeed' in self.data_map:
            self.data_map['inBandwidth'], self.data_map['outBandwidth'], self.data_map['ifBandwidth'] = self.calculate_bandwidth()

    def calculate_bandwidth(self):
        if len(self.data_map['ifInOctets']) < 2 or len(self.data_map['ifOutOctets']) < 2:
            return 0, 0, 0

        last_speed = int(self.data_map['ifSpeed'][-1]['value'])
        time_diff = int(self.data_map['ifInOctets'][-1]['timestamp']) - int(self.data_map['ifInOctets'][-2]['timestamp'])

        if time_diff == 0:
            return 0, 0, 0

        delta_in = int(self.data_map['ifInOctets'][-1]['value']) - int(self.data_map['ifInOctets'][-2]['value'])
        delta_out = int(self.data_map['ifOutOctets'][-1]['value']) - int(self.data_map['ifOutOctets'][-2]['value'])

        in_bandwidth = self.process_speed((delta_in*8*100) / (time_diff))
        out_bandwidth = self.process_speed((delta_out*8*100) / (time_diff))

        total_bandwidth = str(round(((delta_in + delta_out)*8*100) / (time_diff*last_speed/10), 3)) + ' %'

        return in_bandwidth, out_bandwidth, total_bandwidth

    def process_speed(self, speed):
        if speed < 1000:
            return str(speed) + ' bps'
        elif speed < 1000000:
            return str(round(speed / 1000, 3)) + ' Kbps'
        elif speed < 1000000000:
            return str(round(speed / 1000000, 3)) + ' Mbps'
        else:
            return str(round(speed / 1000000000, 3)) + ' Gbps'

    def get_data_in_time(self, tag: str, time_start: int, time_end: int) -> int:
        if ( tag not in self.data_map ):
            return -1

        data = self.data_map[tag]
        if ( len(data) < 2 ):
            return -1
        if ( time_end < data[0]["timestamp"] ):
            return -1
        if ( time_start > data[-1]["timestamp"] ):
            return -1

        i = 0
        while ( time_start > data[i]["timestamp"] ):
            i += 1
        start = int(data[i]["value"])

        i = len(data) - 1
        while ( time_end < data[i]["timestamp"] ):
            i -= 1
        end = int(data[i]["value"])

        return end - start

