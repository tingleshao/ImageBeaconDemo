from subprocess import call
import sys


class data_broadcaster():
    def broadcast_data(self, data):
        # data is a list of bytes
        command = ["sudo", "hcitool", "-i", "hci0", "cmd", "0x08", "0x0008", "1e", "02", "01", "1a", "1a", "ff", "4c", "00", "02", "15"]
        data_str = [(4-len(hex(item))) * '0' + hex(item)[2:] for item in data]
        print("data" + str(data))
        print("datastr" + str(data_str))
        command = command + data_str + ["00", "00", "00", "00"]
        print("command: " + str(command))
        call(command)
