import time
import socket
import pygame
import json

'''
运行电端实读北手数
过okt送据树派
'''

class BeiTongHandleTx:
    def __init__(self, host='192.168.0.101', port=12223):
        self.status = True
        self.client = socket.socket()  # 1.声明协议类型，同时生成socket链接对象
        try:
            self.client.connect((host, port))  # 绑定要监听端口=(服务器的ip地址+任意一个端口)
        except TimeoutError:
            self.status = False
        except OSError:
            self.status = False


        pygame.init()
        pygame.joystick.init()
        try:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
        except pygame.error:
            self.status = False

    def read_handle(self):
        pygame.event.get()
        ret = bytes(json.dumps({
            '1': -int(self.joystick.get_axis(1) * 250),
            '2': +int(self.joystick.get_axis(0) * 250),
            '3': -int(self.joystick.get_axis(3) * 250),
            '4': +int(self.joystick.get_axis(2) * 250),
            '5': self.joystick.get_button(6),
            '6': self.joystick.get_button(7),
        }), encoding='utf-8')
        self.client.send(ret)
        return ret

    def start(self):
        while True:
            data = self.read_handle()
            print(data)
            time.sleep(0.1)


if __name__ == '__main__':
    print("hello.")
    while True:
        ip = input('Please input thde IP:')
        port = input('Please input thde Port:')

        if not ip:
            ip = '192.168.0.101'

        if not port:
            port = 12223

        tmp = BeiTongHandleTx(host=ip, port=port)


        if tmp.status:
            tmp.start()
        else:
            print("connect error.please check the handle or server.")
