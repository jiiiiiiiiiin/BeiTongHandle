import socket
import json
import serial



class AnoDT:
    def __init__(self):
        self.MYHWADDR = 0x05
        self.SWJADDR = 0xAF

        # order
        self.order_control = 0xC6
        self.order_led = 0xC5

        self.led_off = 0x00
        self.led_red = 0x01
        self.led_green = 0x02
        self.led_blue = 0x03
        self.led_yellow = 0x04
        self.led_purple = 0x05
        self.led_cyan = 0x06
        self.led_white = 0x07

        self.BYTE1 = lambda x: (x >> 8) & 0xff
        self.BYTE2 = lambda x: (x >> 0) & 0xff

        self.ser = serial.Serial("/dev/ttyAMA0", 9600)

    def send_control(self, signals):
        data = []
        for signal in signals:
            _temp = int(signal)
            data.append(self.BYTE1(_temp))
            data.append(self.BYTE2(_temp))
        self.order(func=self.order_control, data=data)


    def send_led(self, signal):
        if 0x00 <= signal <= 0x07:
            data = [signal]
        else:
            data = [0x00]
        self.order(func=self.order_led, data=data)


    def order(self, func, data):
        length = len(data) + 1
        data_to_send = [0xAA, self.SWJADDR, self.MYHWADDR, 0xE0, length, func]
        data_to_send.extend(data)

        # sum
        sum_data = 0
        for i in data_to_send:
            sum_data += i

        data_to_send.append(sum_data % 256)
        self.ser.write(bytes(data_to_send))



class BeiTongHandleRx:
    def __init__(self, host='0.0.0.0', port=12223):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.listen(5)
        self.ano = AnoDT()
        

    def start(self):
        print("start listen.")
        while True:
            client, addr = self.server.accept()
            print("accep:{}".format(addr))
            while True:
                try:
                    msg = client.recv(1024)
                except ConnectionResetError:
                    msg = 0
                if msg == 0:
                    break
                try:
                    msg = json.loads(str(msg, encoding='utf-8'))
#                    print(msg)
                    self.ano.send_control([
                        msg.get("1"),
                        msg.get("2"),
                        msg.get("3"),
                        msg.get("4"),
                        msg.get("5"),
                        msg.get("6")
                    ])
                except json.decoder.JSONDecodeError:
                    pass
                

            client.close()




bt = BeiTongHandleRx()
#bt.start()
import time
#while True:
#    for i in range(8):
#        bt.ano.send_led(i)
#        time.sleep(0.5)
#        bt.ano.send_led(0)
#import time
#time.sleep(5)

bt.ano.send_control([0, 10, 0, 0, 1, 0])
time.sleep(1)
bt.ano.send_control([0, 0, 0, 0, 0, 1])

