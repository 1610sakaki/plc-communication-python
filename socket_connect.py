# MELSEC_MCプロトコルを使用してPLC（Programmable Logic Controller）と通信するためのPythonコード

import json
import socket
import sys

# PLCとのソケット通信を行うためのクラス
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
        except Exception:
            return -1

    def myreceive(self):
        print("myreceive")
        data = []
        try:
            data = self.sock.recv(1024)
            return data
        except Exception:
            return -1


# 送信するコマンドを作成するためのクラス
class MakeCommand:
    def __init__(self) -> None:
        json_open = open("melsec.json", "r")
        self.loading = json.load(json_open)

    def socket(self):
        # PLCのIPアドレスとポート番号を取得
        return [val for val in self.loading["socket_settings"].values()]

    def common(self):
        # 読みと書きで共通コマンド部分
        return [val for val in self.loading["common"].values()]

    def read(self):
        # 共通コマンドstrと読み込みコマンドstrを結合させ、一個のコマンドを作成
        cmd = self.common() + [val for val in self.loading["read"].values()]
        print(cmd)
        return "".join(cmd)

    def write(self):
        # 共通コマンドstrと書き込みコマンドstrを結合させ、一個のコマンドを作成
        cmd = self.common() + [val for val in self.loading["write"].values()]
        print(cmd)
        return "".join(cmd)


def main(args):
    mysocket = MySocket()
    mk_cmd = MakeCommand()
    socket = mk_cmd.socket()

    if mysocket.connect(socket[0], int(socket[1])) == 0:  # PLCと通信成功したら実行
        if args == "r":  # 一括読み込みの場合
            print("read")
            read_cmd = mk_cmd.read()
            mysocket.mysend(read_cmd)  # 読み込みコマンド送信

        elif args == "w":  # 一括書き込みの場合
            print("write")
            write_cmd = mk_cmd.write()
            mysocket.mysend(write_cmd)  # 書き込みコマンド送信

        ret = mysocket.myreceive().decode("utf-8")  # 応答伝文
        new_ret = [
            ret[0:4],  # サブヘッダ
            ret[4:6],  # ネットワーク番号
            ret[6:8],  # PC番号
            ret[8:12],  # 要求先ユニットI/O番号
            ret[12:14],  # 要求先ユニット局番号
            ret[14:18],  # 応答データ長
            ret[18:22],  # 終了コード
            ret[22:],  # 読み込みのときは読み出しデータ（のはずだが・・・）
        ]
        print(new_ret)

    else:
        print("Conection Error")
        sys.exit()

    mysocket.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print("Please specify mode (r or w)")
