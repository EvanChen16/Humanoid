// #ifndef TDATAUNIT_H
// #define TDATAUNIT_H
// #include <fstream>
// #include <string>
// #include <stdlib.h>
// #include <string.h>
// #include <usb_cam/tool.hpp>


// struct CameraParameter
// {
//     int  auto_exposure;
//     int  auto_white_balance;
//     int  auto_Backlight_Compensation;
//     int  brightness;
//     int  contrast;
//     int  saturation;
//     int  white_balance;
// };

// class TdataUnit
// {
// public:
//     TdataUnit() { CameraParameterValue = new CameraParameter(); }
//     ~TdataUnit() { delete CameraParameterValue; }
//     void SaveCameraSetFile(std::string location);
//     void LoadCameraSetFile(std::string location);

//     CameraParameter* CameraParameterValue;
// };

// extern TdataUnit* DataUnit;

// #endif // TDATAUNIT_H