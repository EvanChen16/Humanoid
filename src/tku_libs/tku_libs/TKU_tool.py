# import rclpy
import logging
# from rclpy.node import Node
# from rclpy import get_package_share_directory
from ament_index_python.packages import get_package_share_directory
from std_msgs.msg import String
from time import time
import os
import sys
import math
import numpy as np
import time


class Tool():
    def __init__(self):
        # super().__init__('TKU_tool')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # logging.basicConfig(level=logging.INFO)
        self.stand_path = ""
        self.parameterpath = ""
        self.package_path = ''


    def getPackagePath(self, package_name):
        try:
            self.package_Path = get_package_share_directory(package_name)
            if not self.package_Path:
                return "N"
            return self.package_Path  # 返回包的路径
        except Exception as e:
            self.logger.info(f"packagePath is {str(e)}")
            return "N"
        
    def initParameterPath(self):

        self.search = "Desktop/"

        self.loc = self.parameterpath.find(self.search)

        if self.loc != -1:  # 检查是否找到匹配的字符串
            self.src = self.parameterpath
            self.dst = self.stand_path
            self.length = len(self.parameterpath) - len(self.loc) + len(self.search)

            while self.length > 0:
                self.dst += self.src[0]
                self.src = self.src[1:]
                self.length -= 1
            self.dst += '\0'
            self.stand_path += "Standmotion"
        else:
            self.stand_path = "/home/iclab/Desktop/Standmotion"
            # print("parameter_path is", parameter_path)
            # self.logger.info('stand_path is %s', self.stand_path)

    def readvalue(self, fin, title, mode):
        self.sbuffer = ""
        # line = ''
        while True:
            line = fin.readline().strip()  # 讀取一行文字，並去除空白符號

            while line == '---' or line == '':
                line = fin.readline().strip()  # 略過空行或特殊標記

            if len(line) > len(title) and title in line:  # 使用 in 來檢查 title 是否在 line 中
                self.sbuffer = line[line.find(title):line.find(title) + len(title)]
                if '=' in line:
                    sline = line.split('=')[1]  # 使用 split 方法來取得 = 之後的部分
                    extracted_part = sline[1:4]
                    # self.logger.error(sline)
                    # self.logger.error(extracted_part)
                    try:
                        if mode == 0:
                            return int(sline)  # 嘗試將其轉換為整數
                        elif mode == 1:
                            return float(sline)  # 嘗試將其轉換為浮點數
                        elif mode == 2 or mode == 4:
                            return int(extracted_part)
                        elif mode == 3 or mode == 5:
                            return int(extracted_part)
                    except ValueError as e:
                        if mode == 0:
                            self.logger.error('mode 0')
                            self.logger.error('read_value() Error!!')
                            self.logger.error('Invalid integer value!')
                        elif mode == 1:
                            self.logger.error('mode 1')
                            self.logger.error('read_value() Error!!')
                            self.logger.error('Invalid float value!')
                        elif mode == 2 or 4:
                            self.logger.error('mode 2 4')
                            self.logger.error('read_value() Error!!')
                            self.logger.error('Invalid float value!')
                        else:
                            self.logger.error('mode 3 5')
                            self.logger.error('read_value() Error!!')
                            self.logger.error('Invalid integer value!')
                        return -1
                else:
                    self.logger.error('read_value() Error!!')
                    self.logger.error('Please check "=" before and after, must have spaces!!')
                    self.logger.info(line)
                    return -1
            else:
                self.logger.error('read_value() Error!!')
                self.logger.error('Please check your cpp and ini!!')
                self.logger.info('cpp str name is %s', title)
                self.logger.info('ini str name is %s', line)
                return -1


        
    def Delay(self, timedelay):
        start_time = time.time() * 1000  # 獲得當前時間（毫秒）
        end_time = start_time

        while (end_time - start_time) <= timedelay:
            end_time = time.time() * 1000


class ToolInstance(Tool):
    _instance = None  # 类变量用于保存单例对象

    def __init__(self):
        super().__init__()

    @staticmethod
    def getInstance():
        if ToolInstance._instance is None:
            ToolInstance._instance = ToolInstance()
        return ToolInstance._instance

    @staticmethod
    def deleteInstance():
        if ToolInstance._instance is not None:
            ToolInstance._instance = None  # 释放引用，垃圾收集器将负责清理对象


class TimeClass:
    def __init__(self, check_time_ms=1000.0):
        self.check_time_ms = check_time_ms
        self.start = 0.0
        self.end = 0.0
        self.time_ms = 0.0

    def updateTime(self):
        self.end = time.time()
        self.time_ms = 1000.0 * (self.end - self.start)

    def initialize(self):
        self.start = time.time()
        self.end = self.start
        self.time_ms = 0.0

    def setTimerPass(self, check_time_ms, init_flag=True):
        self.check_time_ms = check_time_ms
        if init_flag:
            self.initialize()

    def getTimeMs(self):
        self.updateTime()
        return self.time_ms

    def checkTimePass(self):
        if self.getTimeMs() > self.check_time_ms:
            return True
        else:
            return False

    def getPeriodTimeMs(self):
        return self.check_time_ms
