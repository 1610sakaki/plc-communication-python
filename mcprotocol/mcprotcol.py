# MELSEC_MCプロトコル    PYTHON

import socket


class MySocket:
    def __init__(self, sock=None):
        print("init")
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        print("connect")
        try:
            self.sock.connect((host, port))
            return 0
        except socket.error:
            print("コネクトエラーです")
            return -1

    def close(self):
        print("CLOSE")

        try:
            self.sock.close()
            return 0
        except socket.error:
            print("クロ-ズエラーです")
            return -1

    def mysend(self, msg):
        print("mysend")
        try:
            self.sock.send(msg.encode("utf-8"))
        except:
            return -1

    def myreceive(self):
        print("myreceive")
        data = []
        try:
            data = self.sock.recv(1024)
        except:
            return -1
        return data


# -----------------------------------------------------
def main():
    # IPアドレス  100.100.100.50
    # 自局ポート番号 5010
    host = "100.100.100.50"
    port = 5010
    myapp = MySocket()
    connect_status = myapp.connect(host, port)
    # ワードの読み出し　16ビット符号有り  D0　D1
    if connect_status == 0:
        subheader = "5000"
        net = "00"
        pc = "FF"
        unitio = "03FF"
        unitno = "00"
        nlen = "0018"
        cputimer = "0010"
        command = "0401"
        subcommand = "0000"
        device = "D*000000"
        number = "0002"

        cmd = (
            subheader
            + net
            + pc
            + unitio
            + unitno
            + nlen
            + cputimer
            + command
            + subcommand
            + device
            + number
        )
        myapp.mysend(cmd)
        ret = []
        count = 2
        ret = myapp.myreceive().decode("utf-8")
        datanum = []
        anser = ret[18:22]
        if anser == "0000":
            for i in range(0, count):
                start = 4 * i + 22
                end = 4 * i + 4 + 22
                data = int(ret[start:end], 16)
                if data >= 32767:
                    data = data - 65536
                datanum.append(data)
                print(str(datanum[i]))

    # ワードの読み出し　16ビット符号無し
    if connect_status == 0:
        subheader = "5000"
        net = "00"
        pc = "FF"
        unitio = "03FF"
        unitno = "00"
        nlen = "0018"
        cputimer = "0010"
        command = "0401"
        subcommand = "0000"
        device = "D*000000"
        number = "0002"
        cmd = (
            subheader
            + net
            + pc
            + unitio
            + unitno
            + nlen
            + cputimer
            + command
            + subcommand
            + device
            + number
        )
        myapp.mysend(cmd)
        ret = []
        count = 2
        ret = myapp.myreceive().decode("utf-8")
        datanum = []
        anser = ret[18:22]
        if anser == "0000":
            for i in range(0, count):
                start = 4 * i + 22
                end = 4 * i + 4 + 22
                data = int(ret[start:end], 16)
                datanum.append(data)
                print(str(datanum[i]))
    # ワードの読み出し　32ビット符号無し  D0 D1
    if connect_status == 0:
        subheader = "5000"
        net = "00"
        pc = "FF"
        unitio = "03FF"
        unitno = "00"
        nlen = "0018"
        cputimer = "0010"
        command = "0401"
        subcommand = "0000"
        device = "D*000000"
        number = "0004"
        cmd = (
            subheader
            + net
            + pc
            + unitio
            + unitno
            + nlen
            + cputimer
            + command
            + subcommand
            + device
            + number
        )
        myapp.mysend(cmd)
        ret = []
        count = 2 * 2
        ret = myapp.myreceive().decode("utf-8")
        datanum = []
        anser = ret[18:22]
        if anser == "0000":
            for i in range(0, count, 2):
                start = 4 * i + 22
                end = 4 * i + 4 + 22
                hstart = 4 * i + 26
                hend = 4 * i + 26 + 4
                datalow = int(ret[start:end], 16)
                datahigh = int(ret[hstart:hend], 16)
                data = datahigh * 65536 + datalow
                datanum.append(data)
                print(str(data))
    # ビットの読み出し M0-M3
    if connect_status == 0:
        subheader = "5000"
        net = "00"
        pc = "FF"
        unitio = "03FF"
        unitno = "00"
        nlen = "0018"
        cputimer = "0010"
        command = "0401"
        subcommand = "0001"
        device = "M*000000"
        number = "0004"
        cmd = (
            subheader
            + net
            + pc
            + unitio
            + unitno
            + nlen
            + cputimer
            + command
            + subcommand
            + device
            + number
        )
        myapp.mysend(cmd)
        count = 4
        ret = []
        ret = myapp.myreceive().decode("utf-8")
        datanum = []
        anser = ret[18:22]
        if anser == "0000":
            for i in range(0, count):
                start = i + 22
                data = int(ret[start], 10)
                datanum.append(data)
                print(str(data))
    # ビットの書き込み M0=1  M1=1  M2=0  M3=1
    if connect_status == 0:
        subheader = "5000"
        net = "00"
        pc = "FF"
        unitio = "03FF"
        unitno = "00"
        nlen = "001C"
        cputimer = "0010"
        command = "1401"
        subcommand = "0001"
        device = "M*000000"
        number = "0004"
        devicedata = "1101"
        cmd = (
            subheader
            + net
            + pc
            + unitio
            + unitno
            + nlen
            + cputimer
            + command
            + subcommand
            + device
            + number
            + devicedata
        )
        myapp.mysend(cmd)
        ret = []
        ret = myapp.myreceive().decode("utf-8")
        anser = ret[18:22]
        print(anser)
    # ワードの書き込み
    if connect_status == 0:
        subheader = "5000"
        net = "00"
        pc = "FF"
        unitio = "03FF"
        unitno = "00"
        nlen = "001C"
        cputimer = "0010"
        command = "1401"
        subcommand = "0000"
        device = "D*000002"
        number = "0001"
        # 16進で入力  0010
        devicedata = "0010"
        cmd = (
            subheader
            + net
            + pc
            + unitio
            + unitno
            + nlen
            + cputimer
            + command
            + subcommand
            + device
            + number
            + devicedata
        )
        myapp.mysend(cmd)
        ret = []
        ret = myapp.myreceive().decode("utf-8")
        anser = ret[18:22]
        print(anser)
    myapp.close()


if __name__ == "__main__":
    main()
