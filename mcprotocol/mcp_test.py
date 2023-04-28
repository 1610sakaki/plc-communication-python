#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymcprotocol
import threading
import log  # 自作モジュール
from logging import getLogger
import time


class InspectionThread(threading.Thread):
    def __init__(self):

        # ---- Setting for threading
        super(InspectionThread, self).__init__()
        self.stop_event = threading.Event()
        self.setDaemon(True)
        self.alive = True

        # ---- Setting for log ----
        self.log_path = "./MCProtocol/Log/"
        self.logger = getLogger(__name__)
        log.set_log_config(self.logger, self.log_path, __name__ + ".log")

        # ---- Setting for MC Protocol ----
        self.target_plc_ip = "192.168.1.2"
        self.port = 1025  # Need to set config on PLC side

        # Prepare Mitsubishi Q connection
        self.mc = pymcprotocol.Type3E()

        return

    def __del__(self):
        print("End")

    def stop(self):
        self.stop_event.set()

    def run(self):

        # ---- Start connection ----
        ascii_flag = True
        self.__connect_plc(ascii_flag)

        # ---- Initialize local flag ----
        flag_shoot_done = False

        while not self.stop_event.is_set():

            try:
                # Initialize array for PLC bits
                bitunits_X = []
                bitunits_Y = []

                # Read the number of bitunits from headdevice
                bitunits_X = self.mc.batchread_bitunits(headdevice="X0", readsize=3)
                bitunits_Y = self.mc.batchread_bitunits(
                    headdevice="Y0", readsize=3
                )  # ex. bitunits_Y array [Y0, Y1, Y2]

                # Y0 OFF
                if bitunits_Y[0] == 0:

                    if flag_shoot_done:
                        flag_shoot_done = False

                        self.logger.info("Y0 OFF")
                        bitunits_X[0] = 0
                        self.mc.batchwrite_bitunits(headdevice="X0", values=bitunits_X)
                        self.logger.info(f"Write {bitunits_X}")

                # Y0 ON
                if bitunits_Y[0] == 1:

                    if not flag_shoot_done:
                        flag_shoot_done = True

                        self.logger.info(f"Y0 ON")
                        bitunits_X[0] = 1
                        self.mc.batchwrite_bitunits(headdevice="X0", values=bitunits_X)
                        self.logger.info(f"Write {bitunits_X}")

            except Exception as e:
                self.logger.exception(e)
                self.__disconnect_plc()

                # Delay for restarting
                time.sleep(5)

                self.logger.info("Re-connect")
                self.__connect_plc(ascii_flag)

        self.__disconnect_plc()

    def __connect_plc(self, ascii_flag):

        try:
            if ascii_flag:
                self.mc.setaccessopt(commtype="ascii")

            self.mc.connect(self.target_plc_ip, self.port)
            self.logger.info(f"Connected: IP {self.target_plc_ip}, Port {self.port} ")

        except Exception as e:
            self.logger.exception(e)

    def __disconnect_plc(self):
        try:
            self.mc.close()
            self.logger.info(f"Close connection")

        except Exception as e:
            self.logger.exception(e)


if __name__ == "__main__":

    ith = InspectionThread()

    ith.start()
    time.sleep(20)
    ith.stop()
    ith.join()
