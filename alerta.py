import easysnmp
import time
import numpy as np

class SNMPMonitor:
    def __init__(self, quota, hostname, security_level, security_username, privacy_password, auth_protocol, auth_password, privacy_protocol, version):
        self.session = easysnmp.Session(hostname=hostname, security_level=security_level, security_username=security_username, privacy_password=privacy_password, auth_protocol=auth_protocol, auth_password=auth_password, privacy_protocol=privacy_protocol, version=version)
        self.oid = 'IF-MIB::ifInOctets.1'
        self.quota = quota
        self.alerts = np.empty(shape=[0, 2])

    def get_bytes_count(self):
        response = self.session.get(self.oid)
        return int(response.value)

    def check_quota(self, bytes_count):
        if bytes_count > self.quota:
            return True
        return False

    def log_alert(self, bytes_count):
        timestamp = int(time.time())
        alert = np.array([[bytes_count, timestamp]])
        self.alerts = np.append(self.alerts, alert, axis=0)

    def monitor_quota(self):
        bytes_count = self.get_bytes_count()

        if self.check_quota(bytes_count):
            self.log_alert(bytes_count)
            print(f'Valor de contagem de bytes excedeu a quota permitida. Valor atual: {bytes_count}, {int(self.alerts[-1,1])}')

        else:
            print(f'Valor de contagem de bytes dentro da quota permitida. Valor atual: {bytes_count}')


if __name__ == '__main__':
    # Configurações do dispositivo SNMPv3
    hostname = 'localhost'
    security_level = 'auth_with_privacy'
    security_username = 'MD5DESUser'
    auth_protocol = 'MD5'
    auth_password = 'md51234567'
    privacy_protocol = 'DES'
    privacy_password = 'des1234567'

    # Quota estabelecida
    quota = (2**16)-1

    # Cria uma instância do monitor SNMP
    monitor = SNMPMonitor(quota, hostname, security_level, security_username, privacy_password, auth_protocol, auth_password, privacy_protocol, version=3)

    while True:
        monitor.monitor_quota()
        # printa o np de alertas.
        print(monitor.alerts)
        time.sleep(10)  # Intervalo de 10 segundos entre as consultas SNMP