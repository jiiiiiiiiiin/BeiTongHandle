import socket
import json
import serial

'''
运行于树莓派，通过接受电脑端北通手柄数据，在通过匿名自定义协议发送到飞控端进行控制
'''


class AnoDT:
    def __init__(self):
        self.MYHWADDR = 0x05
        self.SWJADDR = 0xAF

        self.BYTE1 = lambda x: (x >> 8) & 0xff
        self.BYTE2 = lambda x: (x >> 0) & 0xff

        self.ser = serial.Serial("/dev/ttyS0", 115200)

    def send_control(self, signals):
        length = 8
        data_to_send = [0xAA, self.SWJADDR, self.MYHWADDR, 0xE0, length, 0xC6]

        for signal in signals:  # len = 8
            _temp = int(signal * 100)
            data_to_send.append(self.BYTE1(_temp))
            data_to_send.append(self.BYTE2(_temp))

        sum_data = 0
        for i in data_to_send:
            sum_data += i

        data_to_send.append(sum_data % 256)
        self.ser.write(bytes(data_to_send))


class BeiTongHandleRx:
    def __init__(self, host='localhost', port=12223):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.ano = AnoDT()

    def start(self):
        print("start listen.")
        while True:
            client, addr = self.server.accept()
            print("收到来自{}请求".format(addr))
            while True:
                try:
                    msg = client.recv(1024)
                except ConnectionResetError:
                    msg = 0
                if msg == 0:
                    break
                msg = json.loads(str(msg, encoding='utf-8'))
                print(msg)
                self.ano.send_control([
                    msg.get("1"),
                    msg.get("2"),
                    msg.get("3"),
                    msg.get("4")
                ])
            client.close()



if __name__ == '__main__':
    bt = BeiTongHandleRx()
    bt.start()
