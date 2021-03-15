import time
import socket
import pygame
import json

'''
运行于电脑端，实时读取北通手柄数据
通过socket发送数据到树莓派
'''


class BeiTongHandleTx:
    def __init__(self, host='localhost', port=12223):
        self.client = socket.socket()  # 1.声明协议类型，同时生成socket链接对象
        self.client.connect((host, port))  # 绑定要监听端口=(服务器的ip地址+任意一个端口)
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def read_handle(self):
        pygame.event.get()
        ret = bytes(json.dumps({
            '1': -int(self.joystick.get_axis(1) * 250),
            '2': +int(self.joystick.get_axis(0) * 250),
            '3': -int(self.joystick.get_axis(3) * 250),
            '4': +int(self.joystick.get_axis(2) * 250)
        }), encoding='utf-8')
        self.client.send(ret)
        return ret

    def start(self):
        while True:
            data = self.read_handle()
            print(data)
            time.sleep(0.1)


if __name__ == '__main__':
    tmp = BeiTongHandleTx()
    tmp.start()

