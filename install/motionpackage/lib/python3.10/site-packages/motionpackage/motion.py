import rclpy
# import threading
import sys
from rclpy.node import Node
from std_msgs.msg import Bool, Int16, UInt8
import time
import struct
import serial
from serial import SerialException
import array

from tku_libs.TKU_tool import Tool, ToolInstance
######  msgs  ########
from tku_msgs.msg import (
    Parametermessage,
    Walkingmessage,
    HeadPackage,
    SandHandSpeed,
    InterfaceSend2Sector,
    SingleMotorData,
    SaveMotionVector,
    SaveMotion,
    Callback,
    SensorPackage,
    SensorSet,
    PIDpackage,
)
from tku_msgs.srv import(
    CheckSector,
    ReadMotion
)
#####################

SENSOR_SET_PACKAGE_SIZE = 12
IMU_PACKAGE_SIZE = 28
# AX12VELOCITY = 1016949.152542373
tool             = Tool()
timer_sensor_set = ToolInstance()
walkack          = Bool()
interface_ack    = Bool()
execute_ack      = Bool()
FPGAack          = Int16()


class TsRobotis:
    def __init__(self, ID, GoalPosition, Speed):
        ######  motorinit    #########
        self.ID = ID
        self.GoalPosition = GoalPosition
        self.exGoalPosition = 0  # Assuming exGoalPosition is initialized to 0
        self.Speed = Speed
        #############################
class MyNode(Node):
    def __init__(self):
        self.node = rclpy.create_node('motion')
        super().__init__('motionpackage')
        self.serial = serial.Serial()
        self.serial_head = serial.Serial()
        self.serial_IMU = serial.Serial()
        self.declare_parameter('/location', 'default_value')  # 宣告帶有預設值的參數
        self.location = self.get_parameter('/location').get_parameter_value().string_value
        self.read_IMU_count = 0

        self.RobotisList = []
        #####  publisher    #####
        self.FPGAack_Publish             = self.create_publisher(Int16,          "/package/FPGAack",           10)
        self.InterfaceCallBack_Publish   = self.create_publisher(Bool,           "/package/motioncallback",    10)
        self.walkack_Publish             = self.create_publisher(Bool,           "/package/walkack",           10)
        self.ExecuteCallBack_Publish     = self.create_publisher(Bool,           "/package/executecallback",   10)
        self.Sensorpackage_Publish       = self.create_publisher(SensorPackage,  "/package/sensorpackage",     10)
        #########################
        #####  subscriber   #####
        self.parameter_sub               = self.create_subscription(Parametermessage,    "/package/parameterdata",       self.parameterCallback,               1)
        self.motion_sub                  = self.create_subscription(Walkingmessage,      "/package/walkingdata",         self.motionCallBack,                  1)
        self.headmotor_subscribe         = self.create_subscription(HeadPackage,         "/package/HeadMotor",           self.HeadMotorFunction,            1000)
        self.SectorSend2FPGA_subscriber  = self.create_subscription(Int16,               "/package/Sector",              self.SectorSend2FPGAFuction,       1000)
        self.motorspeed_subscribe        = self.create_subscription(SandHandSpeed,       "/package/motorspeed",          self.MotionSpeedFunction,          1000)
        self.SingleMotorData_subscribe   = self.create_subscription(SingleMotorData,     "/package/SingleMotorData",     self.SingleMotorFunction,          1000)
        self.interfaceSend2Sector        = self.create_subscription(InterfaceSend2Sector,"/package/InterfaceSend2Sector",self.InterfaceSend2SectorFunction, 1000)
        self.InterfaceSaveData_Subscribe = self.create_subscription(SaveMotion,          "/package/InterfaceSaveMotion", self.InterfaceSaveDataFunction,    1000)
        self.SensorSet_Subscribe         = self.create_subscription(SensorSet,           "/sensorset",                   self.SensorSetFunction,             100)
        self.PIDcontroll_Subscribe       = self.create_subscription(PIDpackage,          "/package/pidcontroll",         self.motor_setPID,                  100)
        #########################
        ######  service   #######
        self.InterfaceReadData_service      = self.create_service(ReadMotion, '/package/InterfaceReadSaveMotion', self.InterfacereadDataFunction)
        self.InterfaceCheckSector_service   = self.create_service(CheckSector, '/package/InterfaceCheckSector', self.InterfaceCheckSectorFunction)
        #########################
        ######  packageinit  ####
        self.PIDpackage         = [0] * 14
        self.parameterpackage   = [0] * 31
        self.motorpackage       = [0] * 19
        self.package_init()
        #########################
        self.sectorpackage      = [0] * 5
        #########################
        ######  sync_write  #####
        self.torquePackage      = [0] * 13
        self.HeadPackage        = [0] * 32
        #########################
        self.onemotorpackage    = [0] * 87
        self.packageEnd         = [0x4E, 0x45]
        self.sensorsetpackage   = [0] * SENSOR_SET_PACKAGE_SIZE
        self.savemotor9         = [0, 0, 0]
        self.InterfaceFlag      = 0
        #########################
        ######  serial    #######
        # self.serial      = None
        # self.serial_head = None
        # self.serial_IMU  = None
        #########################
        #########
        self.packageMotorData   = [0] * 87
        self.parameterPath      = ""
        self.SendSectorPackage  = []            # 用于保存 unsigned int 的列表
        ##########################

        # self.mcssl_init()  # 在初始化节点时调用 mcssl_init

        ########  IMU  ##########
        self.Desire_Roll    = 0
        self.Desire_Pitch   = 0
        self.Desire_Yaw     = 0
        #########################

        self.walkack            = Bool()
        self.interface_ack      = Bool()
        self.execute_ack        = Bool()
        self.FPGAack            = Int16()
        self.sensor_data_buf    = bytearray(IMU_PACKAGE_SIZE)

        self.SaveSectorPackage  = []            # 用于保存 unsigned int 的列表
        self.handspeedpackage   = []            # 用于保存 unsigned int 的列表
        self.IMUPackage         = bytearray()   # 用于保存 unsigned char 的字节数组
        self.CheckSectorPackage = []            # 用于保存 int 的列表
        self.dio_tmpstatus      = 0
        self.walkdata_receive   = False

    def RobotisListini(self):
        self.RobotisList.clear()
        for i in range(1, 3):
            motor = TsRobotis(i, 2048, 511)
            self.RobotisList.append(motor)
        print("aaaaa")

    def sync_write(self):
        ######  torque_package  #########
        self.torque_package     = [0] * 13
        self.torque_package[0]  = 0xFF
        self.torque_package[1]  = 0xFF
        self.torque_package[2]  = 0xFD
        self.torque_package[3]  = 0x00
        self.torque_package[4]  = 0xFE
        self.torque_package[5]  = 0x06
        self.torque_package[6]  = 0
        self.torque_package[7]  = 0x03
        self.torque_package[8]  = 0x40
        self.torque_package[9]  = 0
        self.torque_package[10] = 0x01
        blk_size    = 5 + self.torquePackage[5]
        crc_value   = self.update_crc(self.torquePackage[:blk_size])  # 這裡計算CRC值
        self.torquePackage[11] = crc_value & 0xFF
        self.torquePackage[12] = (crc_value >> 8)
        for cnt in self.torque_package :
            self.serial_head.write(bytes([cnt]))
        #################################
        tool.Delay(1)
        ######  head_package  ###########
        self.head_package       = [0] * 32
        self.head_package[0]    = 0xFF
        self.head_package[1]    = 0xFF
        self.head_package[2]    = 0xFD
        self.head_package[3]    = 0x00
        self.head_package[4]    = 0xFE
        self.head_package[5]    = 0x19
        self.head_package[6]    = 0
        self.head_package[7]    = 0x83
        self.head_package[8]    = 0x70
        self.head_package[9]    = 0
        self.head_package[10]   = 0x08
        self.head_package[11]   = 0
        for index, motor in enumerate(self.RobotisList):  # 假設這裡有兩個 RobotisList 項目
            base_index = 12 + (index * 9)  # 計算起始索引
            self.head_package[base_index]    = motor.ID
            self.head_package[base_index +1] = motor.Speed & 0xFF
            self.head_package[base_index +2] = (motor.Speed >> 8) & 0xFF 
            self.head_package[base_index +3] = (motor.Speed >> 16) & 0xFF 
            self.head_package[base_index +4] = (motor.Speed >> 24) & 0xFF 
            self.head_package[base_index +5] = motor.GoalPosition
            self.head_package[base_index +6] = (motor.GoalPosition >> 8) & 0xFF 
            self.head_package[base_index +7] = (motor.GoalPosition >> 16) & 0xFF 
            self.head_package[base_index +8] = (motor.GoalPosition >> 24) & 0xFF 
        blk_size    = 5 + self.head_package[5]
        crc_value   = self.update_crc(self.head_package[:blk_size])  # 這裡計算CRC值
        self.head_package[30] = crc_value & 0xFF
        self.head_package[31] = (crc_value >> 8)
        for cnt in self.head_package:
            self.serial_head.write(bytes([cnt]))
    
    def HeadMotorFunction(self, msg):
        self.RobotisList[msg.id - 1].GoalPosition = msg.position
        self.RobotisList[msg.id - 1].Speed = msg.speed
        self.sync_write()

    def standini(self):
        # self.packageMotorData = [0] * 87  # 初始化 packageMotorData 數組

        print("Standini")

        pathend = "/sector/"
        pathend2 = "29.ini"
        path = tool.stand_path + pathend + pathend2
        print(path)

        try:
            with open(path, 'r') as fin:
                # print("209")
                packagecnt = int(tool.readvalue(fin, "PackageCnt", 0))
                # print("211")
                SendSectorPackage = int(tool.readvalue(fin, "Package", 2))
                # print("213")
                for i in range(1, packagecnt):
                    SendSectorPackage.append(int(tool.readvalue(fin, "|", 3)))
                self.packageMotorData[0] = 0x53
                self.packageMotorData[1] = 0x54
                self.packageMotorData[2] = 0xF2
                self.packageMotorData[3:packagecnt + 3] = SendSectorPackage[1:]
                self.serial.write(self.packageMotorData[:packagecnt + 3])
        except FileNotFoundError:
            print("Filename Error!!")
        except Exception as e:
            pass
        print("End_LoadSector")

    def SectorSend2FPGAFuction(self, msg):
        print("SendSectorPackage")
        filename = str(msg)
        pathend = "/sector/"
        pathend2 = ".ini"
        path = ""
        if msg.data == 29:
            path = tool.stand_path + pathend + filename + pathend2
        else:
            path = tool.getPackagePath(self.parameterPath) + "/Parameter" + filename + pathend2
        try:
            with open(path, 'r') as fin:
                packagecnt = int(tool.readvalue(fin, "PackageCnt", 0))
                self.SendSectorPackage.append(tool.readvalue(fin, "Package", 2))
                print(f"mode = {self.SendSectorPackage[0]}")
                for i in range(1, packagecnt):
                    self.SendSectorPackage.append(tool.readvalue(fin, "|", 3))

            if self.SendSectorPackage[0] == 241:
                self.packageMotorData[0] = 0x53
                self.packageMotorData[1] = 0x54
                self.packageMotorData[2] = 0xF4
                for i in range(1, packagecnt):
                    self.packageMotorData[cnt] = self.SendSectorPackage[i]
                    cnt += 1
                self.serial.write(self.packageMotorData[:cnt])
                self.execute_ack.data = True
                self.ExecuteCallBack_Publish.publish(self.execute_ack.data)
                print("241_Execute is finsih")
            elif self.SendSectorPackage[0] == 242:
                self.packageMotorData[0] = 0x53
                self.packageMotorData[1] = 0x54
                self.packageMotorData[2] = 0xF2
                for i in range(1, packagecnt):
                    self.packageMotorData[cnt] = self.SendSectorPackage[i]
                    cnt += 1
                self.serial.write(self.packageMotorData[:cnt])
                self.execute_ack.data = True
                self.ExecuteCallBack_Publish.publish(self.execute_ack)
                print("242_Execute is finsih")
            elif self.SendSectorPackage[0] == 243:
                self.packageMotorData[0] = 0x53
                self.packageMotorData[1] = 0x54
                self.packageMotorData[2] = 0xF3
                for i in range(1, packagecnt):
                    self.packageMotorData[cnt] = self.SendSectorPackage[i]
                    cnt += 1
                self.serial.write(self.packageMotorData[:cnt])
                self.execute_ack.data = True
                self.ExecuteCallBack_Publish.publish(self.execute_ack)
                print("243_Execute is finsih")
            elif self.SendSectorPackage[0] == 244:
                motionlist_flag = True 
                cnt_tmp = 1
                while motionlist_flag:
                    self.packageMotorData[0] = 0x53
                    self.packageMotorData[1] = 0x54
                    self.packageMotorData[2] = 0xF3
                    for i in range(cnt_tmp, packagecnt):
                        self.packageMotorData[cnt] = self.SendSectorPackage[i]
                        cnt += 1
                        if self.SendSectorPackage[i+1] == 68 and self.SendSectorPackage[i+2] == 89:
                            cnt_tmp = i + 4
                            if self.SendSectorPackage[cnt_tmp] == 69 and self.SendSectorPackage[cnt_tmp + 1] == 78:
                                motionlist_flag = False
                            self.serial.write(self.packageMotorData[:cnt])
                            print(f"Delay: {self.SendSectorPackage[i + 3]}")
                            tool.Delay(self.SendSectorPackage[i + 3])
                            cnt = 3
                            break
                            
                self.execute_ack.data = True
                self.ExecuteCallBack_Publish.publish(self.execute_ack)
                print("244_Execute is finsih")
        except FileNotFoundError:
            print("Filename Error!!")
        except Exception as e:
            print("An error occurred:", e)
        print("End_LoadSector")
        self.SendSectorPackage.clear()

    def InterfaceSaveDataFunction(self, msg):
        self.motiondata = SaveMotionVector()
        self.motiondata.savemotionvector.append(msg)
        if msg.saveflag:
            print("VectorSize =", len(self.motiondata.savemotionvector) - 1)
            filename = msg.name
            pathend = "/"
            path = ""

            if msg.savestate == 1:
                path = tool.stand_path
                path += pathend
                path += filename
            else:
                path = tool.getPackagePath(self.parameterPath)
                path += "/Parameter"
                path += pathend
                path += filename

            with open(path, 'w') as out_file:
                print("SaveBegin")
                out_file.write(f"VectorCnt = {len(self.motiondata.savemotionvector) - 1}\n")
                for i in range(len(self.motiondata.savemotionvector)):
                    motion = self.motiondata.savemotionvector[i]
                    if motion.motionstate == 0:
                        out_file.write(f"State = {motion.motionstate}\n")
                        out_file.write(f"ID = {motion.ID}\n")

                        for j in range(len(motion.motionlist)):
                            if j % 2 == 0:
                                out_file.write(f"A{(j//2) + 1} = {motion.motionlist[j]}|")
                            else:
                                out_file.write(f"D{(j//2) + 1} = {motion.motionlist[j]}")
                                if j == len(motion.motionlist) - 1:
                                    break
                                else:
                                    out_file.write("|")
                        out_file.write("\n")
                    elif motion.motionstate in [1, 2, 3, 4]:
                        for j, value in enumerate(motion.motordata):
                            out_file.write(f"M{j+1} = {value}")
                            if j < len(motion.motordata) - 1:
                                out_file.write("|")
                            else:
                                out_file.write("\n")

                print("SaveEnd")
                self.motiondata.savemotionvector.clear()
                    
    def InterfacereadDataFunction(self, request, response):
        print("LoadParameter")
        filename = request.name
        pathend = "/"
        path = ""
        # str_val = ""
        # datacnt = 0
        num = 0

        if request.readstate == 1:
            path = tool.stand_path
            pathend += filename
            path += pathend
        else:
            path = tool.getPackagePath(self.parameterPath)
            path += "/Parameter"
            pathend += filename
            path += pathend
        try:    
            with open(path, "r") as file:
                print("Start_Load")
                response.vectorcnt = tool.readvalue(file, "VectorCnt", 0)
                for i in range(response.vectorcnt):
                    response.motionstate.append(tool.readvalue(file, "State", 0))
                    response.id.append(tool.readvalue(file, "ID", 0))
                    state = response.motionstate[i]
                    if state == 0:
                        for j in range(40):
                            if (j + 1) % 2 == 1:
                                motion = f"A{(j / 2) + 1}"
                                num = tool.readvalue(file, motion, 2)
                            else:
                                delay = f"D{(j / 2) + 1}"
                                if j == 39:
                                    num = tool.readvalue(file, delay, 0)
                                else:
                                    num = tool.readvalue(file, delay, 2)
                            response.motionlist.append(num)
                        break
                    elif state == 1:
                        for j in range(21):
                            motor = f"M{j+1}"
                            if j == 20:
                                num = tool.readvalue(file, motor, 0)
                            else:
                                num = tool.readvalue(file, motor, 2)
                            response.relativedata.append(num)
                        break
                    elif state == 2:
                        for j in range(21):
                            motor = f"M{j+1}"
                            if j == 20:
                                num = tool.readvalue(file, motor, 0)
                            else:
                                num = tool.readvalue(file, motor, 2)
                            response.relativedata.append(num)
                        break
                    elif state == 3:
                        for j in range(21):
                            motor = f"M{j+1}"
                            if j == 20:
                                num = tool.readvalue(file, motor, 0)
                            else:
                                num = tool.readvalue(file, motor, 2)
                            response.absolutedata.append(num)
                        break
                    elif state == 4:
                        for j in range(21):
                            motor = f"M{j+1}"
                            if j == 20:
                                num = tool.readvalue(file, motor, 0)
                            else:
                                num = tool.readvalue(file, motor, 2)
                            response.absolutedata.append(num)
                        break
                print("End_Load")
                return True
        except Exception as e:
            print("Error:", e)
            return False

    def InterfaceCheckSectorFunction(self, requst, response):
        print("CheckSectorStart")
        filename = str(requst.data)
        pathend = "/sector/"
        pathend2 = ".ini"
        path = ""
        packagecnt = 0
        returnvalue = 0
        motionlist_flag = True
        cnt_tmp = 84

        if requst.data == 29:
            path = tool.stand_path  # Assuming tool is an object available in the context
            path += pathend + filename + pathend2
            print("447")
        else:
            path = tool.getPackagePath(self.parameterPath) + "/Parameter" + filename + pathend2
            print("450")
        with open(path, 'r') as fin:
            if not fin:
                print("Filename Error!!")
            else:
                print("453")
                packagecnt = tool.readvalue(fin, "PackageCnt", 0)
                returnvalue = tool.readvalue(fin, "Package", 4)
                if returnvalue != -1:
                    self.CheckSectorPackage.append(returnvalue)
                else:
                    response.checkflag = False
                    return True
                print("mode =", self.CheckSectorPackage[0])
                for i in range(1, packagecnt):
                    returnvalue = tool.readvalue(fin, "|", 5)
                    if returnvalue != -1:
                        self.CheckSectorPackage.append(returnvalue)
                    else:
                        response.checkflag = False
                        return True
                if self.CheckSectorPackage[0] in [241, 242, 243]:
                    if packagecnt != 85:
                        print("\033[0;31m242 243 Packagecnt is not correct!!\033[0m")
                        response.checkflag = False
                        return True
                    print(f"Sector {requst.data} is correct!!")
                    print("CheckSectorEnd")
                    response.checkflag = True
                    return True

                elif self.CheckSectorPackage[0] == 244:
                    while motionlist_flag:
                        if cnt_tmp + 5 > packagecnt:
                            print("\033[0;31m244 count of Package is not the same as Packagecnt!!\033[0m")
                            response.checkflag = False
                            return True
                        if self.CheckSectorPackage[cnt_tmp + 1] == 68 and self.CheckSectorPackage[cnt_tmp + 2] == 89:
                            if self.CheckSectorPackage[cnt_tmp + 4] == 69 and self.CheckSectorPackage[cnt_tmp + 5] == 78:
                                motionlist_flag = False
                            cnt_tmp += 87
                        else:
                            print("\033[0;31m244 Package have not 68 89!!\033[0m")
                            response.checkflag = False
                            return True
                    print(f"Sector {requst.data} is correct!!")
                    print("CheckSectorEnd")
                    response.checkflag = True
                    return True
                else:
                    print(f"\033[0;31m{self.SendSectorPackage} is not correct mode!!\033[0m")
                    response.checkflag = False
                    return True

    def InterfaceSend2SectorFunction(self, msg):
        packageData = msg.package
        self.SaveSectorPackage.extend(packageData)
        length = len(self.SaveSectorPackage)

        if(
            self.SaveSectorPackage[0] == 0x53
            and self.SaveSectorPackage[1] == 0x54
            and self.SaveSectorPackage[length - 2] == 0x4E
            and self.SaveSectorPackage[length - 1] == 0x45
        ):
            pathend = "/sector"
            pathend2 = ".ini"
            path = f"{pathend}/{msg.sectorname}{pathend2}"
            if msg.sectorname == "29":
                path = f"{tool.stand_path}/{msg.sectorname}{pathend2}"
            else:
                path = f"{tool.getPackagePath(self.parameterPath)}/Parameter/{msg.sectorname}{pathend2}"

            with open(path, "w") as OutFile:
                print("SaveSectorBegin")
                OutFile.write(f"PackageCnt = {self.SaveSectorPackage[length - 3]}\n")
                OutFile.write(f"Package = {self.SaveSectorPackage[2]} || ")
                pkgsum = 1
                self.interface_ack.data = True  # 这一行没具体的上下文，需要确认
                if self.SaveSectorPackage[2] in [241, 242, 243]:
                    if self.SaveSectorPackage[length - 3] == 85:
                        print("Send sector is successful!!")
                        self.interface_ack.data = True
                    else:
                        print("Send sector is fail!!")
                        self.interface_ack.data = False
                    self.InterfaceCallBack_Publish.publish(self.interface_ack)
                for i in range(3, self.SaveSectorPackage[length - 3] + 2):  # [0]&[1] is headpackage so +2 to save last package
                    if self.SaveSectorPackage[2] == 244:
                        if self.SaveSectorPackage[i + 1] == 68 and self.SaveSectorPackage[i + 2] == 89:
                            print(f"pkgsum = {pkgsum}")
                            if pkgsum == 84 or pkgsum == 87:
                                pkgsum = 1
                                self.interface_ack.data = True
                            else:
                                print("Send sector is fail!!")
                                self.interface_ack.data = False
                                self.InterfaceCallBack_Publish.publish(self.interface_ack)
                        else:
                            if i == self.SaveSectorPackage[length - 3] + 1:
                                print("Send sector is successful!!")
                                self.InterfaceCallBack_Publish.publish(self.interface_ack)
                            pkgsum += 1

                    if not self.interface_ack.data:
                        break

                    OutFile.write(str(self.SaveSectorPackage[i]) + "|| ")

                print("SaveSectorEnd")
                self.SaveSectorPackage.clear()
                OutFile.close()

    def motor_setPID(self,msg):
        motor_P_L = msg.motor_p & 0xFF
        motor_P_H = (msg.motor_p >> 8) & 0xFF
        motor_I_L = msg.motor_i & 0xFF
        motor_I_H = (msg.motor_i >> 8) & 0xFF
        motor_D_L = msg.motor_d & 0xFF
        motor_D_H = (msg.motor_d >> 8) & 0xFF

        self.PIDpackage[4] = msg.motorid

        self.get_logger().info("ID:%d, set_P:%d, set_I:%d, set_D:%d" % (msg.motorid, msg.motor_p, msg.motor_i, msg.motor_d))
        self.get_logger().info("P:%d, I:%d, D:%d" % (msg.pflag, msg.iflag, msg.dflag))

        # Parameter
        if msg.pflag:
            self.PIDpackage[8] = 0x54
            self.PIDpackage[10] = motor_P_L
            self.PIDpackage[11] = motor_P_H
        elif msg.iflag:
            self.PIDpackage[8] = 0x52
            self.PIDpackage[10] = motor_I_L
            self.PIDpackage[11] = motor_I_H
        elif msg.dflag:
            self.PIDpackage[8] = 0x50
            self.PIDpackage[10] = motor_D_L
            self.PIDpackage[11] = motor_D_H

            self.PIDpackage[9] = 0

        blk_size = 5 + self.PIDpackage[5]

        crc = self.update_crc(0, bytes(self.PIDpackage[:blk_size]))  # 假設這個函數會返回 CRC 值

        self.PIDpackage[12] = crc & 0xFF
        self.PIDpackage[13] = (crc >> 8) & 0xFF

        # for cnt in range(14):
        self.serial.write(bytes([self.PIDpackage]))
            
    def mcssl_init(self):
        tool.initParameterPath()
        devs_head = "/dev/ttyS1"
        devs_IMU = "/dev/ttyS0"
        if not self.serial.is_open or not self.serial_head.is_open or not self.serial_IMU.is_open:
            print("serial = ",self.serial.is_open)
            print("head = ",self.serial_head.is_open)
            print("IMU = ",self.serial_IMU.is_open)
            try:
                self.mcssl_callback()
                # self.serial_head    = serial.Serial(port=devs_head,baudrate=115200, bytesize=8,parity='N',stopbits=1,timeout=1)
                # print("head = ",self.serial_head.is_open)
                # self.head_callback()
                # self.serial_IMU     = serial.Serial(port=devs_IMU,baudrate=115200, bytesize=8,parity='N',stopbits=1)
                # print("IMU = ",self.serial_IMU.is_open)
                # self.IMU_callback()
                # print(f"Initialize Motion with port={devs}...")
            except serial.SerialException as e:
                print(str(e))
                print("---> Motion RS232 OPEN FAIL <---")
                return -1
        return 1
    def mcssl_finish(self):
        self.serial.close()
        self.serial_head.close()
        self.serial_IMU.close()

    def head_callback(self):
        pass

    def IMU_callback(self):
        got_imu_package_flag = False
        index = 0

        for i in range(length):
            self.IMUPackage.append(buf[i])

        if len(self.IMUPackage) >= IMU_PACKAGE_SIZE:
            for i in range(len(self.IMUPackage)):
                if (self.IMUPackage[i] == 0x53 and self.IMUPackage[i+1] == 0x54 and 
                    self.IMUPackage[i+2] == 0xF7 and self.IMUPackage[i+IMU_PACKAGE_SIZE-1]):
                    index = i
                    got_imu_package_flag = True

            if got_imu_package_flag:
                for i in range(IMU_PACKAGE_SIZE):
                    self.sensor_data_buf[i] = self.IMUPackage[index+i]

            self.Sensor_Data_Process()
            self.IMUPackage.clear()

    def mcssl_callback(self):
        devs = "/dev/ttyUSB0"
        self.serial = serial.Serial(port=devs,baudrate=115200, bytesize=8,parity='N',stopbits=1,timeout=0.1)
        print("serial = ",self.serial.is_open)
        while True:
            received_lines = self.serial.readlines()
            if received_lines:
                for line in received_lines:
                    hex_values = ' '.join([format(byte, '02X') for byte in line])
                    print(hex_values)
                    #wait 1 second
                    time.sleep(1)
        self.walkdata_receive = False
        self.dio_tmpstatus = 0
        # buf = [0] * 4
        i = 0
        # print(f"FPGAack is :{hex_values[0]:x} {hex_values[1]:x} {hex_values[2]:x} {hex_values[3]:x}")
        
        # for i in range(4):
        #     # print('fuck')
        #     # print(buf[i])nnㄙ
        #     if self.dio_tmpstatus == 0 and buf[i] == ord('S'):
        #         self.dio_tmpstatus = 1
        #         print('aa')
        #     elif self.dio_tmpstatus == 1:
        #         if buf[i] == ord('U'):
        #             print('bb')
        #             self.dio_tmpstatus = 2
        #         elif buf[i] == ord('T'):
        #             print('cc')
        #             self.dio_tmpstatus = 4
        #     elif self.dio_tmpstatus == 2:
        #         print('dd')
        #         self.dio_tmpstatus = 3
        #         self.FPGAack.data = buf[i]
        #         self.FPGAack_Publish.publish(self.FPGAack)
        #         print(f"FPGAack is :{buf[i]:x}")
        #     elif self.dio_tmpstatus == 3 and buf[i] == ord('E'):
        #         print('ee')
        #         self.dio_tmpstatus = 0
        #         if self.walkdata_receive:
        #             print('ff')
        #             self.walkack.data = True
        #             self.walkack_Publish.publish(self.walkack)
        #     elif self.dio_tmpstatus == 4:
        #         print('gg')
        #         if buf[i] == ord('Y'):
        #             self.InterfaceFlag = 1
        #         elif buf[i] == ord('N'):
        #             print('hh')
        #             self.InterfaceFlag = 0
        #             self.SendSectorPackage.clear()
        #         elif buf[i] == 0xF5:
        #             print('ii')
        #             self.walkdata_receive = True
        #         else:
        #             print('jj')
        #             self.walkdata_receive = False
        #         self.dio_tmpstatus = 3

    def update_crc(crc_accum, data_blk_ptr, data_blk_size):
        crc_table = [
            0x0000, 0x8005, 0x800F, 0x000A, 0x801B, 0x001E, 0x0014, 0x8011,
            0x8033, 0x0036, 0x003C, 0x8039, 0x0028, 0x802D, 0x8027, 0x0022,
            0x8063, 0x0066, 0x006C, 0x8069, 0x0078, 0x807D, 0x8077, 0x0072,
            0x0050, 0x8055, 0x805F, 0x005A, 0x804B, 0x004E, 0x0044, 0x8041,
            0x80C3, 0x00C6, 0x00CC, 0x80C9, 0x00D8, 0x80DD, 0x80D7, 0x00D2,
            0x00F0, 0x80F5, 0x80FF, 0x00FA, 0x80EB, 0x00EE, 0x00E4, 0x80E1,
            0x00A0, 0x80A5, 0x80AF, 0x00AA, 0x80BB, 0x00BE, 0x00B4, 0x80B1,
            0x8093, 0x0096, 0x009C, 0x8099, 0x0088, 0x808D, 0x8087, 0x0082,
            0x8183, 0x0186, 0x018C, 0x8189, 0x0198, 0x819D, 0x8197, 0x0192,
            0x01B0, 0x81B5, 0x81BF, 0x01BA, 0x81AB, 0x01AE, 0x01A4, 0x81A1,
            0x01E0, 0x81E5, 0x81EF, 0x01EA, 0x81FB, 0x01FE, 0x01F4, 0x81F1,
            0x81D3, 0x01D6, 0x01DC, 0x81D9, 0x01C8, 0x81CD, 0x81C7, 0x01C2,
            0x0140, 0x8145, 0x814F, 0x014A, 0x815B, 0x015E, 0x0154, 0x8151,
            0x8173, 0x0176, 0x017C, 0x8179, 0x0168, 0x816D, 0x8167, 0x0162,
            0x8123, 0x0126, 0x012C, 0x8129, 0x0138, 0x813D, 0x8137, 0x0132,
            0x0110, 0x8115, 0x811F, 0x011A, 0x810B, 0x010E, 0x0104, 0x8101,
            0x8303, 0x0306, 0x030C, 0x8309, 0x0318, 0x831D, 0x8317, 0x0312,
            0x0330, 0x8335, 0x833F, 0x033A, 0x832B, 0x032E, 0x0324, 0x8321,
            0x0360, 0x8365, 0x836F, 0x036A, 0x837B, 0x037E, 0x0374, 0x8371,
            0x8353, 0x0356, 0x035C, 0x8359, 0x0348, 0x834D, 0x8347, 0x0342,
            0x03C0, 0x83C5, 0x83CF, 0x03CA, 0x83DB, 0x03DE, 0x03D4, 0x83D1,
            0x83F3, 0x03F6, 0x03FC, 0x83F9, 0x03E8, 0x83ED, 0x83E7, 0x03E2,
            0x83A3, 0x03A6, 0x03AC, 0x83A9, 0x03B8, 0x83BD, 0x83B7, 0x03B2,
            0x0390, 0x8395, 0x839F, 0x039A, 0x838B, 0x038E, 0x0384, 0x8381,
            0x0280, 0x8285, 0x828F, 0x028A, 0x829B, 0x029E, 0x0294, 0x8291,
            0x82B3, 0x02B6, 0x02BC, 0x82B9, 0x02A8, 0x82AD, 0x82A7, 0x02A2,
            0x82E3, 0x02E6, 0x02EC, 0x82E9, 0x02F8, 0x82FD, 0x82F7, 0x02F2,
            0x02D0, 0x82D5, 0x82DF, 0x02DA, 0x82CB, 0x02CE, 0x02C4, 0x82C1,
            0x8243, 0x0246, 0x024C, 0x8249, 0x0258, 0x825D, 0x8257, 0x0252,
            0x0270, 0x8275, 0x827F, 0x027A, 0x826B, 0x026E, 0x0264, 0x8261,
            0x0220, 0x8225, 0x822F, 0x022A, 0x823B, 0x023E, 0x0234, 0x8231,
            0x8213, 0x0216, 0x021C, 0x8219, 0x0208, 0x820D, 0x8207, 0x0202
        ]
        for j in range(data_blk_size):
            i = ((crc_accum >> 8) ^ data_blk_ptr[j]) & 0xFF
            crc_accum = (crc_accum << 8) ^ crc_table[i]
        return crc_accum

    def sensor_data_process(self):
        self.Sensor_Data_tmp = [0] * 11
        self.IMU_Value = [0.0] * 3
        self.ForceSensor_Value_tmp = [0] * 8
        self.ForceSensor_Value = [0] * 8
        self.Sensor_Data_Count = 3
        self.isDataOk = False
        self.sensorpackage = SensorPackage()
        self.forward_Sector_Number = 78
        self.backward_Sector_Number = 87

        for i in range(3):
            self.Sensor_Data_tmp[i] = (self.sensor_data_buf[self.Sensor_Data_Count] << 8) | self.sensor_data_buf[self.Sensor_Data_Count + 1]
            self.Sensor_Data_Count += 2

            if self.Sensor_Data_tmp[i] & 0x8000:  # Check if the number is negative
                self.IMU_Value[i] = float(~(self.Sensor_Data_tmp[i] & 0x7FFF) + 1) / 100.0
            else:
                self.IMU_Value[i] = float(self.Sensor_Data_tmp[i]) / 100.0

            self.sensorpackage.imudata.append(self.IMU_Value[i])
        self.Sensor_Data_Count += 1
        self.Sensor_Data_Count += 1  # 跳過保留的封包位元組
        for i in range(8):
            ForceSensor_Value_tmp = (self.sensor_data_buf[self.Sensor_Data_Count] << 8) | self.sensor_data_buf[self.Sensor_Data_Count + 1]
            self.Sensor_Data_Count += 2

            if ForceSensor_Value_tmp & 0x8000:  # 檢查數字是否為負數
                ForceSensor_Value = ((ForceSensor_Value_tmp & 0x7FFF) * (-1))
            else:
                ForceSensor_Value = ForceSensor_Value_tmp & 0xFFFF

            self.sensorpackage.forcesensordata.append(ForceSensor_Value)
        # 發布處理後的數據
        self.Sensorpackage_Publish.publish(self.sensorpackage)
        self.sensorpackage.imudata.clear()
        self.sensorpackage.forcesensordata.clear()

    def SensorSetFunction(self, msg):
        setopt = msg.sensor_modeset
        Desire_parameter = [0, 0, 0]

        if setopt & 0x02:
            Desire_parameter = [msg.sensor_p, msg.sensor_i, msg.sensor_d]
        elif setopt & 0x08:
            Desire_parameter = [msg.roll, msg.pitch, 0]
        elif setopt & 0x10 or setopt & 0x20 or setopt & 0x40:
            Desire_parameter = [msg.sensor_p, msg.sensor_i, msg.sensor_d]
        elif setopt & 0x80:
            Desire_parameter = [msg.sup_f, msg.nsup_f, 0]
        else:
            Desire_parameter = [0, 0, 0]
        self.sensorsetpackage[0] = 0x53
        self.sensorsetpackage[1] = 0x54
        self.sensorsetpackage[2] = 0xF6

        for i in range(3):
            if Desire_parameter[i] < 0:
                Desire_parameter[i] = ~(Desire_parameter[i]) + 1
                self.sensorsetpackage[3 + i * 2] = ((Desire_parameter[i] >> 8) & 0xFF) | 0x80
                self.sensorsetpackage[4 + i * 2] = Desire_parameter[i] & 0xFF
                Desire_parameter[i] = ~(Desire_parameter[i] - 1)
            else:
                self.sensorsetpackage[3 + i * 2] = (Desire_parameter[i] >> 8) & 0xFF
                self.sensorsetpackage[4 + i * 2] = Desire_parameter[i] & 0xFF

        self.sensorsetpackage[9] = setopt
        self.sensorsetpackage[10] = 0  # Reserve
        self.sensorsetpackage[11] = 0x45

        tool.Delay(10)
        self.serial_IMU.write(bytearray(self.sensorsetpackage))
        ToolInstance.initialize()

    def AutoSensorSetFunction(self):
        # cssl = self.mcssl_init()
        Desire_Set = True
        IMU_Reset = False
        ForceState = False
        Gain_Set = False
        SENSOR_SET_PACKAGE_SIZE = 12
        sensorsetpackage = bytearray(SENSOR_SET_PACKAGE_SIZE)
        sensorsetpackage[0] = 0x53
        sensorsetpackage[1] = 0x54
        sensorsetpackage[2] = 0xF6
        Desire_Roll     = 0  # 你需要设定 Desire_Roll 的实际值
        Desire_Pitch    = 0  # 你需要设定 Desire_Pitch 的实际值
        Desire_Yaw      = 0  # 你需要设定 Desire_Yaw 的实际值

        if Desire_Roll < 0:
            Desire_Roll = ~(Desire_Roll) + 1
            sensorsetpackage[3] = ((Desire_Roll >> 8) & 0xFF) | 0x80
            sensorsetpackage[4] = Desire_Roll & 0xFF
            Desire_Roll = ~(Desire_Roll - 1)
        else:
            sensorsetpackage[3] = (Desire_Roll >> 8) & 0xFF
            sensorsetpackage[4] = Desire_Roll & 0xFF

        if Desire_Pitch < 0:
            Desire_Pitch = ~(Desire_Pitch) + 1
            sensorsetpackage[5] = ((Desire_Pitch >> 8) & 0xFF) | 0x80
            sensorsetpackage[6] = Desire_Pitch & 0xFF
            Desire_Pitch = ~(Desire_Pitch - 1)
        else:
            sensorsetpackage[5] = (Desire_Pitch >> 8) & 0xFF
            sensorsetpackage[6] = Desire_Pitch & 0xFF

        if Desire_Yaw < 0:
            Desire_Yaw = ~(Desire_Yaw) + 1
            sensorsetpackage[7] = ((Desire_Yaw >> 8) & 0xFF) | 0x80
            sensorsetpackage[8] = Desire_Yaw & 0xFF
            Desire_Yaw = ~(Desire_Yaw - 1)
        else:
            sensorsetpackage[7] = (Desire_Yaw >> 8) & 0xFF
            sensorsetpackage[8] = Desire_Yaw & 0xFF
        if ToolInstance.checkTimePass():
                #     self.serial_IMU.write(bytearray(self.sensorsetpackage))
                #     ToolInstance.initialize()
                sensorsetpackage[9] = (Gain_Set << 3) | (ForceState << 2) | (IMU_Reset << 1) | Desire_Set
                sensorsetpackage[10] = 0
                sensorsetpackage[11] = 0x45
                hex_string = ' '.join([format(byte, '02X') for byte in sensorsetpackage])

                print(hex_string)
        time.sleep(0.1)
        # 将数据以十六进制形式发送到串口
        # ser.write(hex_string)mcssl_init
        # if ToolInstance.checkTimePass():
        #     self.serial_IMU.write(bytearray(self.sensorsetpackage))
        #     ToolInstance.initialize()

    def MotionSpeedFunction(self, msg):
        H = (msg.speed >> 8) & 0xFF
        L = msg.speed & 0xFF

        self.handspeedpackage.clear()

        print("ReadHandMotionStart")
        filename = str(msg.sector)
        pathend = "/sector/"
        pathend2 = ".ini"
        path = tool.getPackagePath(self.parameterPath) + "/Parameter" + pathend + filename + pathend2
        packagecnt = 0
        # cnt = 3

        with open(path, 'r') as fin:
            if fin:
                try:
                    packagecnt = tool.readvalue(fin, "PackageCnt", 0)
                    self.handspeedpackage.append(packagecnt)
                    self.handspeedpackage.append(tool.readvalue(fin, "Package", 2))
                    print(f"mode = {self.handspeedpackage[1]}")
                    for i in range(1, packagecnt):
                        self.handspeedpackage.append(tool.readvalue(fin, "|", 3))
                except Exception as e:
                    pass

        print("End_LoadSector")

        self.handspeedpackage[18] = L
        self.handspeedpackage[19] = H
        self.handspeedpackage[117] = L
        self.handspeedpackage[118] = H

        with open(path, 'w') as OutFile:
            print("SendhandspeedBegin")
            OutFile.write(f"PackageCnt = {self.handspeedpackage[0]}\n")
            OutFile.write("Package = ")
            for i in range(1, self.handspeedpackage[0] + 1):  # [0]&[1] is headpackage so +2 to save the last package
                OutFile.write(f"{self.handspeedpackage[i]}|| ")
                print(f"{self.handspeedpackage[i]}")

            print("SendhandspeedEnd")

        self.handspeedpackage.clear()

    def SingleMotorFunction(self, msg):
        Angle_H, Angle_L, Speed_H, Speed_L = 0, 0, 0, 0
        position = abs(msg.position)
        cnt = 0
        self.onemotorpackage = [0] * 87  # Initialize list of length 87 with zeros

        if msg.position < 0:
            Angle_L = position & 0xFF
            Angle_H = (position >> 8 & 0xFF) + 128
        else:
            Angle_L = position & 0xFF
            Angle_H = position >> 8 & 0xFF

        Speed_L = msg.speed & 0xFF
        Speed_H = msg.speed >> 8 & 0xFF

        self.onemotorpackage[0] = 0x53
        self.onemotorpackage[1] = 0x54
        self.onemotorpackage[2] = 0xF3

        for cnt in range(3, (msg.id - 1) * 4 + 3):
            self.onemotorpackage[cnt] = 0

        self.onemotorpackage[cnt] = Speed_L
        self.onemotorpackage[cnt + 1] = Speed_H
        self.onemotorpackage[cnt + 2] = Angle_L
        self.onemotorpackage[cnt + 3] = Angle_H

        for i in range(cnt + 4, 87):
            self.onemotorpackage[i] = 0

        for i in range(87):
            print("onemotorpackage =", self.onemotorpackage[i])

        self.serial.write(bytes(self.onemotorpackage))

###########################################################################

    def package_init(self):
        self.parameterpackage[0] = 0x53
        self.parameterpackage[1] = 0x54
        self.parameterpackage[2] = 0xF5
        self.parameterpackage[5] = 6
        self.parameterpackage[30] = 0x45

        self.motorpackage[0] = 0x53
        self.motorpackage[1] = 0x54
        self.motorpackage[2] = 0xF5
        self.motorpackage[3] = 1
        self.motorpackage[5] = 3  # data length is 3 bytes
        self.motorpackage[18] = 0x45

        self.PIDpackage[0] = 0xFF
        self.PIDpackage[1] = 0xFF
        self.PIDpackage[2] = 0xFD
        self.PIDpackage[3] = 0x00
        # self.PIDpackage[4] = motorID
        self.PIDpackage[5] = 0x07
        self.PIDpackage[6] = 0
        self.PIDpackage[7] = 0x3

    def convert_to_bytes(self, value):
        value_int = int(value * 100.0)
        if value < 0:
            return struct.pack('>h', value_int)  # big-endian signed short
        else:
            return struct.pack('>H', value_int)  # big-endian unsigned short

    def paradata_send2fpga(self, walking_mode, x_swing, y_swing, z_swing, period_t1, period_t2, sample_time, lock_range, base_default_z, y_swing_shift, x_swing_com, base_lift_z, rightfoot_shift_z, com_y_swing, now_stand_height, now_com_height, stand_balance):
        # x_swing_h, x_swing_l = self.convert_to_bytes(x_swing)
        y_swing_h, y_swing_l = self.convert_to_bytes(y_swing)
        # z_swing_h, z_swing_l = self.convert_to_bytes(z_swing)
        # x_swing_com_h, x_swing_com_l = self.convert_to_bytes(x_swing_com)
        # y_swing_shift_h, y_swing_shift_l = self.convert_to_bytes(y_swing_shift)
        base_lift_z_h, base_lift_z_l                = self.convert_to_bytes(base_lift_z)
        rightfoot_shift_z_h, rightfoot_shift_z_l    = self.convert_to_bytes(rightfoot_shift_z)
        com_y_swing_h, com_y_swing_l                = self.convert_to_bytes(com_y_swing)
        now_stand_height_h, now_stand_height_l      = self.convert_to_bytes(now_stand_height)
        now_com_height_h, now_com_height_l          = self.convert_to_bytes(now_com_height)

        base_default_z_h, base_default_z_l  = struct.pack('>H', int(base_default_z * 100.0))  # big-endian unsigned short
        period_t1_h, period_t1_l            = struct.pack('>H', period_t1)  # big-endian unsigned short
        period_t2_h, period_t2_l            = struct.pack('>H', period_t2)  # big-endian unsigned short

        # Populate parameterpackage
        self.parameterpackage[6] = com_y_swing_h
        self.parameterpackage[7] = com_y_swing_l
        self.parameterpackage[8] = y_swing_h
        self.parameterpackage[9] = y_swing_l
        self.parameterpackage[10] = rightfoot_shift_z_h
        self.parameterpackage[11] = rightfoot_shift_z_l
        self.parameterpackage[12] = period_t1_h
        self.parameterpackage[13] = period_t1_l
        self.parameterpackage[14] = period_t2_h
        self.parameterpackage[15] = period_t2_l
        self.parameterpackage[16] = sample_time & 0xFF
        self.parameterpackage[17] = int(lock_range * 100.0) & 0xFF
        self.parameterpackage[18] = base_default_z_h
        self.parameterpackage[19] = base_default_z_l
        self.parameterpackage[20] = base_lift_z_h
        self.parameterpackage[21] = base_lift_z_l
        self.parameterpackage[22] = now_stand_height_h
        self.parameterpackage[23] = now_stand_height_l
        self.parameterpackage[24] = now_com_height_h
        self.parameterpackage[25] = now_com_height_l
        self.parameterpackage[26] = walking_mode & 0xFF
        self.parameterpackage[27] = 0  # reserve
        self.parameterpackage[28] = 0  # reserve
        self.parameterpackage[29] = 1 if stand_balance else 0  # reserve (bool converted to int)
        self.serial.write(self.parameterpackage)

    def parameterCallback(self, msg):
        x_swing            = msg.x_swing_range
        y_swing            = msg.y_swing_range
        z_swing            = msg.z_swing_range
        period_t1          = msg.period_t
        period_t2          = msg.period_t2
        sample_time        = msg.sample_time
        lock_range         = msg.osc_lockrange
        base_default_z     = msg.base_default_z
        y_swing_shift      = msg.y_swing_shift
        x_swing_com        = msg.x_swing_com
        base_lift_z        = msg.base_lift_z
        rightfoot_shift_z  = msg.rightfoot_shift_z
        com_y_swing        = msg.com_y_swing
        now_stand_height   = msg.now_stand_height
        now_com_height     = msg.now_com_height
        walking_mode       = msg.walking_mode
        stand_balance      = msg.stand_balance
        # if walking_mode not in [9, 10]:
        self.paradata_send2fpga(
            walking_mode,x_swing, y_swing, z_swing, 
            period_t1, period_t2, sample_time, lock_range, 
            base_default_z, y_swing_shift, x_swing_com, 
            base_lift_z, rightfoot_shift_z, com_y_swing,
            now_stand_height, now_com_height, stand_balance
        )
        # else:
        #     self.paradata_send2fpga_2(
        #         walking_mode, y_swing, period_t1)#, kick_point_x, kick_point_y, kick_point_z, back_point_x, back_point_z, support_foot_upper_hip_pitch, kick_foot_ankle_upper_pitch)

##########################################################################


##########################################################################
    def walkingdata_send2fpga(self, x, y, z, theta, walking_cmd, sensor_mode):
        x_h, x_l = self.convert_to_bytes(x)
        y_h, y_l = self.convert_to_bytes(y)
        z_h, z_l = self.convert_to_bytes(z)
        theta_h, theta_l = self.convert_to_bytes(theta)
        
        self.motorpackage[6] = x_h
        self.motorpackage[7] = x_l
        self.motorpackage[8] = y_h
        self.motorpackage[9] = y_l
        self.motorpackage[10] = z_h
        self.motorpackage[11] = z_l
        self.motorpackage[12] = theta_h
        self.motorpackage[13] = theta_l
        self.motorpackage[14] = walking_cmd
        self.motorpackage[15] = sensor_mode
        self.motorpackage[16] = 0  # reserve
        self.motorpackage[17] = 0  # reserve

    def motionCallBack(self, msg):
        x = msg.x
        y = msg.y
        z = msg.z
        theta = msg.theta
        walking_cmd = msg.walking_cmd
        sensor_mode = msg.sensor_mode
        self.walkingdata_send2fpga(x, y, z, theta, walking_cmd, sensor_mode)
        tool.Delay(50)

##########################################################################

    def run(self):
        self.parameterPath = self.location
        print(self.parameterPath)
        tstart = time.time()
        while rclpy.ok():
            if self.mcssl_init() > 0:
                self.standini()
                break
            else:
                time.sleep(1)  # Sleep for 1 second

        print("Motion is running")

        while rclpy.ok():
            if self.read_IMU_count >= 3:  # 60/4 = 15Hz
                self.AutoSensorSetFunction()
                self.read_IMU_count = 0
            else:
                self.read_IMU_count += 1

            # Your logic here...

            rclpy.spin_once(self.node)
            time.sleep(1.0 / 60)


        self.mcssl_finish()

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    node.RobotisListini()
    node.package_init()
    node.run()
    rclpy.shutdown()
if __name__ == '__main__':
    main()