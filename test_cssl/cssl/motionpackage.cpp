#include "motionpackage.h"

static void IMU_callback(int id, uint8_t *buf, int length)
{
    for(int i=0; i<length; i++)
        IMUPackage.push_back(buf[i]);
        printf("IMUcallback is :%x %x %x %x \n",buf[0],buf[1],buf[2],buf[3]);
}

static void mcssl_callback(int id, uint8_t *buf, int length)
{
    printf("FPGAack is :%x %x %x %x \n",buf[0],buf[1],buf[2],buf[3]);
   
}

int mcssl_init()
{
    char *devs;
    char *devs_IMU;
    cssl_start();
    
    if (!serial)
    {
        serial=cssl_open("/dev/ttyUSB0", mcssl_callback, 0, 115200, 8, 0, 1);
    }
    if (!serial_IMU)
    {
        serial_IMU=cssl_open("/dev/ttyS0", IMU_callback, 0, 115200, 8, 0, 1);
    }

    if (!serial)
    {
        printf("%s\n",cssl_geterrormsg());
        printf("---> Motion RS232 OPEN FAIL <---\n");
        fflush(stdout);
        return -1;
    }
    
    if (!serial_IMU)
    {
        printf("%s\n",cssl_geterrormsg());
        printf("---> Head RS232 OPEN FAIL <---\n");
        fflush(stdout);
        return -1;
    }
    cssl_setflowcontrol(serial, 0, 0);
    cssl_setflowcontrol(serial_IMU, 0, 0);
    return 1;
}

void mcssl_finish()
{

    cssl_close(serial);
    cssl_close(serial_IMU);
    cssl_stop();
}
//------------------------


int main(int argc, char **argv)
{
    if(mcssl_init() > 0)
    {
        printf("Motion is ready\n");

        while(1) {
            // 檢查 IMUPackage 中的值
            if (!IMUPackage.empty()) {
                // 有新值
                printf("Received IMU data\n");
                // 在這裡處理 IMUPackage 中的值，例如取出並處理最新的 IMU 數值
                // 這裡可以根據你的需求進行相應的處理

                // 處理完後清空 IMUPackage
                IMUPackage.clear();
            }

            usleep(1000000); // 等待一段時間再進行下一次檢查
        }
    }
    else
    {
        printf("Motion initialization failed\n");
    }

    mcssl_finish();

    return 0;
}