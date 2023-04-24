# 导入套接字模块
import os
import socket
# 导入线程模块
import threading
import constant
import matplotlib.pyplot as plt
# 设置刻度值之间步长(间隔)
from matplotlib.pyplot import MultipleLocator
import tensorflow as tf

# 创建一个折线图
fig = plt.figure(figsize=(16, 12), dpi=120)
# 设置中文语言
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False
# 创建两个表格，211代表创建2行1列，当前在1的位置
ax = fig.add_subplot(2, 2, 1)  # 4区
bx = fig.add_subplot(2, 2, 2)  # 13
cx = fig.add_subplot(2, 2, 3)  # 3区
dx = fig.add_subplot(2, 2, 4)  # 14区


# 定义个函数,使其专门重复处理客户的请求数据（也就是重复接受一个用户的消息并且重复回答，直到用户选择下线）
def dispose_client_request(tcp_client_1, tcp_client_address):
    constant.init()
    initPlt()
    # 5 循环接收和发送数据
    while True:
        recv_data = tcp_client_1.recv(4096)
        if len(constant.m4) > 500:
            constant.init()
            ax.cla()
            bx.cla()
            cx.cla()
            dx.cla()
            plt.cla()
            initPlt()
        if recv_data:
            msg_str = recv_data.hex()
            msg_list = splitStringToByteList(msg_str)
            # print("接收到的数据：",msg_list)
            msg_len = len(msg_list)
            for index in range(0, msg_len):
                if msg_list[index] == 'ff':
                    if index + 2 < msg_len - 1:
                        if msg_list[index + 1] == '01':
                            if (msg_list[index + 2]) == '0c':
                                msg_data = ' '.join(msg_list[index + 5:index + 7]).replace(' ', '')
                                str_3 = msg_list[index + 3]
                                if len(msg_data) != 0:
                                    data = int(msg_data, 16)
                                    if str_3 == '04':
                                        constant.m4.append(data)
                                        ax.plot(list(range(len(constant.m4))), constant.m4, '-r', label='4区')
                                    if str_3 == '0d':
                                        constant.m13.append(data)
                                        bx.plot(list(range(len(constant.m13))), constant.m13, '-g', label='13区')
                                    if str_3 == '03':
                                        constant.m2.append(data)
                                        cx.plot(list(range(len(constant.m2))), constant.m2, '-r', label='2区')
                                    if str_3 == '0e':
                                        print("第14区间16进制转10进制：%s-%d", (msg_data, data))
                                        constant.m15.append(data)
                                        dx.plot(list(range(len(constant.m15))), constant.m15, '-g', label='14区')

        else:
            print("%s 客户端下线了..." % tcp_client_address[1])
            tcp_client_1.close()
            break
        plt.draw()
        plt.pause(0.03)


def splitStringToByteList(bytesString):
    bytesList = []
    for i in range(int(len(bytesString) / 2)):
        bytesList.append(bytesString[i * 2:i * 2 + 2])
    return bytesList


# 给表的Y轴位置加上标签，rotation代表让文字横着展示，labelpad代表文字距表格多远了
def initPlt():
    ax.set_ylabel('4区', rotation=0, fontsize=16, labelpad=20)
    bx.set_ylabel('13区', rotation=0, fontsize=16, labelpad=20)
    cx.set_ylabel('3区', rotation=0, fontsize=16, labelpad=20)
    dx.set_ylabel('14区', rotation=0, fontsize=16, labelpad=20)
    ax.yaxis.set_major_locator(MultipleLocator(2000))
    bx.yaxis.set_major_locator(MultipleLocator(2000))
    cx.yaxis.set_major_locator(MultipleLocator(2000))
    dx.yaxis.set_major_locator(MultipleLocator(2000))
    ax.set_ylim(0, 70000)
    bx.set_ylim(0, 70000)
    cx.set_ylim(0, 70000)
    dx.set_ylim(0, 70000)
    ax.grid(True)
    bx.grid(True)
    cx.grid(True)
    dx.grid(True)


if __name__ == '__main__':
    # 1 创建服务端套接字对象
    tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 设置端口复用，使程序退出后端口马上释放
    tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    # 2 绑定端口
    tcp_server.bind(("", 9999))

    # 3 设置监听
    tcp_server.listen(5)

    # 4 循环等待客户端连接请求（也就是最多可以同时有5个用户连接到服务器进行通信）
    while True:
        tcp_client_1, tcp_client_address = tcp_server.accept()
        # 创建多线程对象
        # thd = threading.Thread(target=dispose_client_request, args=(tcp_client_1, tcp_client_address))
        # draw()
        # 设置守护主线程  即如果主线程结束了 那子线程中也都销毁了  防止主线程无法退出
        # thd.setDaemon(True)

        # 启动子线程对象
        # thd.start()
        dispose_client_request(tcp_client_1, tcp_client_address)

    # 7 关闭服务器套接字 （其实可以不用关闭，因为服务器一直都需要运行）
    # tcp_server.close()
