### 北通手柄控制

- 通过`pygame.joystick`来读取北通手柄数据，通过`socket`发送到树莓派，树莓派读取数据后通过串口发送至飞控进行控制。

- `pyinstaller`打包`pyinstaller -F client.py -p C:\Users\admin\.conda\envs\py\Lib\site-packages\pygame`

  