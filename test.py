from datetime import datetime
from pprint import pprint
from typing import Dict

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException
)


class DeviceBackup:
    """
    Class which backup gns3 devices using ssh.
    """

    def __init__(self, device: Dict):
        self.ssh = self._ssh_connection(device)

    def _ssh_connection(self, device):
        """
        Establish a ssh connection to the device.
        """
        try:
            ssh = ConnectHandler(**device)
            ssh.enable()
            return ssh
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as err:
            print(err)

    def _device_backup(self):
        """
        Send backup commands.
        """
        self.ssh.send_command('terminal length 0')
        output = self.ssh.send_command('show running-config')
        return output

    def print_configuration(self):
        """
        Print device's configuration and store it in a file.
        """
        output = self._device_backup()
        pprint(output, width=80)

        out_file_name = f"backup_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        with open(out_file_name, 'w') as file:
            file.write(output)


if __name__ == '__main__':
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.100.36",
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco",
    }

    conn = DeviceBackup(device)
    conn.print_configuration()
