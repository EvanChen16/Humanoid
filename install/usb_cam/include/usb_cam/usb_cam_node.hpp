// Copyright 2021 Evan Flynn
// Copyright 2014 Robert Bosch, LLC
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are met:
//
//    * Redistributions of source code must retain the above copyright
//      notice, this list of conditions and the following disclaimer.
//
//    * Redistributions in binary form must reproduce the above copyright
//      notice, this list of conditions and the following disclaimer in the
//      documentation and/or other materials provided with the distribution.
//
//    * Neither the name of the Evan Flynn nor the names of its
//      contributors may be used to endorse or promote products derived from
//      this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
// ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
// LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
// CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
// SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
// INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
// CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
// ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
// POSSIBILITY OF SUCH DAMAGE.

#ifndef TDATAUNIT_H
#define TDATAUNIT_H
#ifndef USB_CAM__USB_CAM_NODE_HPP_
#define USB_CAM__USB_CAM_NODE_HPP_

#include <memory>
#include <string>
#include <vector>

#include "camera_info_manager/camera_info_manager.hpp"
#include "image_transport/image_transport.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_srvs/srv/set_bool.hpp"
#include "tku_msgs/msg/camera.hpp"
#include "usb_cam/usb_cam.hpp"
#include "tku_msgs/srv/camera_info.hpp"
#include "usb_cam/tdataunit.hpp"



#include <fstream>
// #include <string>
#include <stdlib.h>
#include <string.h>
// #include <usb_cam/tool.hpp>


#ifndef TOOL_H
#define TOOL_H

#include <ament_index_cpp/get_package_share_directory.hpp>
// #include <rclcpp/rclcpp.hpp>
#include <sys/time.h>
// #include <fstream>
#include <sstream>
#include <cmath>
// #include <vector>
#include <iostream>
// #include <string>

class Tool
{
    public:
        Tool();
        ~Tool();
        std::string getPackagePath(std::string package_name);
        float readvalue(std::fstream &fin, std::string title, int mode);
    public:
        std::string parameterPath;
    private:
        std::string packagePath;
};

class ToolInstance : public Tool
{
    public:
        ToolInstance() : Tool() {}
        ~ToolInstance() {}
        static ToolInstance* getInstance();
        static void deleteInstance();  // 新增這行

    private:
        static ToolInstance *m_pInstance;
};

#endif // TOOL_H




struct CameraParameter
{
    std::string ParameterName;  // 新增這行
    int  auto_exposure;
    int  auto_white_balance;
    int  auto_Backlight_Compensation;
    int  brightness;
    int  contrast;
    int  saturation;
    int  white_balance;
};

class TdataUnit
{
public:
    TdataUnit(); //{ CameraParameterValue = new CameraParameter(); }
    ~TdataUnit(); //{ delete CameraParameterValue; }
    void SaveCameraSetFile(std::string location);
    void LoadCameraSetFile(std::string location);

    CameraParameter* CameraParameterValue;
    ToolInstance* tool;  // 新增這行

};

extern TdataUnit* DataUnit;

#endif // TDATAUNIT_H



std::ostream & operator<<(std::ostream & ostr, const rclcpp::Time & tm)
{
  ostr << tm.nanoseconds();
  return ostr;
}


namespace usb_cam
{

class UsbCamNode : public rclcpp::Node
{
public:
  explicit UsbCamNode(const rclcpp::NodeOptions & node_options);
  ~UsbCamNode();
  void loadcamerasetfile();
  void savecamerasetfile();
  void init();
  void get_params();
  void assign_params(const std::vector<rclcpp::Parameter> & parameters);
  void set_v4l2_params();
  void update();
  void camera_param_callback(const tku_msgs::msg::Camera &msg);
  bool callcamerainfofunction(
    const std::shared_ptr<tku_msgs::srv::CameraInfo::Request> request,
    std::shared_ptr<tku_msgs::srv::CameraInfo::Response> response);
  bool take_and_send_image();
  int brightness_;
  int contrast_;
  int saturation_;
  int white_balance_;
  int exposure_;
  bool auto_focus_;
  bool auto_white_balance_;
  bool auto_exposure_;
  rcl_interfaces::msg::SetParametersResult parameters_callback(
    const std::vector<rclcpp::Parameter> & parameters);

  void service_capture(
    const std::shared_ptr<rmw_request_id_t> request_header,
    const std::shared_ptr<std_srvs::srv::SetBool::Request> request,
    std::shared_ptr<std_srvs::srv::SetBool::Response> response);

  void getFilePath();  // Add this line

  UsbCam * m_camera;

  sensor_msgs::msg::Image::SharedPtr m_image_msg;
  image_transport::CameraPublisher m_image_publisher;

  parameters_t m_parameters;

  sensor_msgs::msg::CameraInfo::SharedPtr m_camera_info_msg;
  std::shared_ptr<camera_info_manager::CameraInfoManager> m_camera_info;

  rclcpp::TimerBase::SharedPtr m_timer;

  rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr m_service_capture;
  rclcpp::node_interfaces::OnSetParametersCallbackHandle::SharedPtr m_parameters_callback_handle;

private:
  rclcpp::Subscription<tku_msgs::msg::Camera>::SharedPtr sub_camera_param_;
  rclcpp::Service<tku_msgs::srv::CameraInfo>::SharedPtr srv_camera_info_;

  TdataUnit CameraSet;
  std::string location;
  std::string file_path_;  // Add this line
};

}  // namespace usb_cam
#endif  // USB_CAM__USB_CAM_NODE_HPP_
