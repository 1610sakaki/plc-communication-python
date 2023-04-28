#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import time
from logging import DEBUG, INFO, FileHandler, Formatter, StreamHandler, getLogger
from logging.handlers import TimedRotatingFileHandler

import pymcprotocol

# 接続設定
TARGET_PLC_IP = "192.168.1.50"
PORT = 5015

# 先頭デバイスアドレス
HEAD_X = "D0"
HEAD_Y = "Y0"


def main():

    # Mitsubishi Qシリーズに接続
    pymc = pymcprotocol.Type3E()
    connect_plc(pymc)

    # フラグ初期化
    flag_work_done = False

    try:
        while True:

            try:

                # 配列初期化
                bitunits_Xs = []
                bitunits_Ys = []

                # PLCのXとYをそれぞれ0から16点読み出し
                bitunits_Xs = pymc.batchread_bitunits(headdevice=HEAD_X, readsize=16)
                bitunits_Ys = pymc.batchread_bitunits(headdevice=HEAD_Y, readsize=16)

                # オルタネート回路
                alternate_circuit(pymc, bitunits_Xs, bitunits_Ys)

            except Exception as e:
                logger.error(f"def main: {e}")
                pymc.close()
                time.sleep(5)
                logger.info("再接続開始")

                connect_plc(pymc)

    except Exception as e:
        logger.error(f"main: {e}")

    finally:
        pymc.close()
        logger.info("終了")


### PLCと接続
def connect_plc(pymc):

    try:
        pymc.connect(TARGET_PLC_IP, PORT)
        logger.info("PLC接続完了")

    except Exception as e:
        logger.error(f"def connect_plc: {e}")


def alternate_circuit(pymc, bitunits_Xs, bitunits_Ys):

    global flag_work_done

    if bitunits_Ys[0] == 0:
        flag_work_done = False  # ワンショットメモリ

    # XがOFFなら1回だけX0をONにしてX0から16点書き込み
    if bitunits_Ys[0] == 1 and bitunits_Xs[0] == 0 and not flag_work_done:
        flag_work_done = True
        logger.debug(f"Y0 ON検出: {bitunits_Ys}")
        bitunits_Xs[0] = 1
        pymc.batchwrite_bitunits(headdevice=HEAD_X, values=bitunits_Xs)
        logger.debug(f"X0 ON書き込み: {bitunits_Xs}")

    # X0がONなら1回だけX0をOFFにしてX0から16点書き込み
    if bitunits_Ys[0] == 1 and bitunits_Xs[0] == 1 and not flag_work_done:
        flag_work_done = True
        logger.debug(f"Y0 ON検出: {bitunits_Ys}")
        bitunits_Xs[0] = 0
        pymc.batchwrite_bitunits(headdevice=HEAD_X, values=bitunits_Xs)
        logger.debug(f"X0 OFF書き込み: {bitunits_Xs}")


### ログ出力
def set_log_config(logger):

    # Log出力先フォルダ
    LOG_PATH = "MCProtocol/Log/"
    os.makedirs(LOG_PATH, exist_ok=True)  # フォルダが無い場合は作成

    # handler1 ターミナル用
    handler1 = StreamHandler()
    handler1.setLevel(DEBUG)
    handler1.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))

    # handler2 ファイル出力用
    filename = LOG_PATH + "MCProtocol.log"
    handler2 = TimedRotatingFileHandler(
        filename=filename, encoding="utf-8", when="midnight", backupCount=30
    )
    handler2.setLevel(INFO)
    handler2.setFormatter(Formatter("%(asctime)s %(levelname)8s %(message)s"))

    logger.info(f"set_log_config: Path = {filename}")

    # loggerにハンドラ設定
    logger.setLevel(DEBUG)
    logger.addHandler(handler1)
    logger.addHandler(handler2)
    logger.propagate = False

    return logger


#### Log Config ####
logger = getLogger(__name__)
logger = set_log_config(logger)
## End of Log config


#### Start ####
if __name__ == "__main__":
    main()
