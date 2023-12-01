// #define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <termios.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <sys/time.h>

#include <pthread.h>
#include <semaphore.h>
#include <math.h>
#include <vector>
#include <boost/program_options.hpp>
#include "cssl.h"
#include "port.h"
#include "cssl.c"


//---save
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
using namespace std;
//---save




#define SENSOR_SET_PACKAGE_SIZE 12
#define IMU_PACKAGE_SIZE 28

using std::string;
cssl_t *serial;
cssl_t *serial_IMU;


vector<unsigned char> IMUPackage;
vector<int> CheckSectorPackage;
struct timeval tstart, tend;
double timeuse;
uint8_t PIDpackage[31] = {0};
uint8_t parameterpackage[31] = {0};
uint8_t motorpackage[19] = {0};
uint8_t HeadPackage[32] = {0};
uint8_t sectorpackage[5] = {0};
uint8_t torquePackage[13] = {0};
uint8_t onemotorpackage[87] = {0};
uint8_t packageMotorData[87] = {0}; 	// address||R MotorSum (id angleL angleH speedL speedH)*MotorSum DelayL DelayH checksum2
uint8_t packageEnd[2] = {0x4E, 0x45};	// N E
uint8_t sensorsetpackage[SENSOR_SET_PACKAGE_SIZE] = {0};
unsigned int savemotor9[3] = {0};
int InterfaceFlag = 0;


bool isBufFull = false;
int sensor_data_buf_cnt = 0;
uint8_t sensor_data_buf[IMU_PACKAGE_SIZE] = {0};

bool fall_Down_Flag = false;
bool old_fall_Down_Flag = false;

char parameterPath[20];

int Desire_Roll = 0;
int Desire_Pitch = 0;
int Desire_Yaw = 0;
int read_IMU_count = 0;