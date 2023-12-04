// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tku_msgs:msg/SensorSet.idl
// generated code does not contain a copyright notice

#ifndef TKU_MSGS__MSG__DETAIL__SENSOR_SET__BUILDER_HPP_
#define TKU_MSGS__MSG__DETAIL__SENSOR_SET__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tku_msgs/msg/detail/sensor_set__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tku_msgs
{

namespace msg
{

namespace builder
{

class Init_SensorSet_sensor_modeset
{
public:
  explicit Init_SensorSet_sensor_modeset(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  ::tku_msgs::msg::SensorSet sensor_modeset(::tku_msgs::msg::SensorSet::_sensor_modeset_type arg)
  {
    msg_.sensor_modeset = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_nsup_f
{
public:
  explicit Init_SensorSet_nsup_f(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_sensor_modeset nsup_f(::tku_msgs::msg::SensorSet::_nsup_f_type arg)
  {
    msg_.nsup_f = std::move(arg);
    return Init_SensorSet_sensor_modeset(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_sup_f
{
public:
  explicit Init_SensorSet_sup_f(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_nsup_f sup_f(::tku_msgs::msg::SensorSet::_sup_f_type arg)
  {
    msg_.sup_f = std::move(arg);
    return Init_SensorSet_nsup_f(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_yaw
{
public:
  explicit Init_SensorSet_yaw(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_sup_f yaw(::tku_msgs::msg::SensorSet::_yaw_type arg)
  {
    msg_.yaw = std::move(arg);
    return Init_SensorSet_sup_f(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_pitch
{
public:
  explicit Init_SensorSet_pitch(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_yaw pitch(::tku_msgs::msg::SensorSet::_pitch_type arg)
  {
    msg_.pitch = std::move(arg);
    return Init_SensorSet_yaw(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_roll
{
public:
  explicit Init_SensorSet_roll(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_pitch roll(::tku_msgs::msg::SensorSet::_roll_type arg)
  {
    msg_.roll = std::move(arg);
    return Init_SensorSet_pitch(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_sensor_d
{
public:
  explicit Init_SensorSet_sensor_d(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_roll sensor_d(::tku_msgs::msg::SensorSet::_sensor_d_type arg)
  {
    msg_.sensor_d = std::move(arg);
    return Init_SensorSet_roll(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_sensor_i
{
public:
  explicit Init_SensorSet_sensor_i(::tku_msgs::msg::SensorSet & msg)
  : msg_(msg)
  {}
  Init_SensorSet_sensor_d sensor_i(::tku_msgs::msg::SensorSet::_sensor_i_type arg)
  {
    msg_.sensor_i = std::move(arg);
    return Init_SensorSet_sensor_d(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

class Init_SensorSet_sensor_p
{
public:
  Init_SensorSet_sensor_p()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SensorSet_sensor_i sensor_p(::tku_msgs::msg::SensorSet::_sensor_p_type arg)
  {
    msg_.sensor_p = std::move(arg);
    return Init_SensorSet_sensor_i(msg_);
  }

private:
  ::tku_msgs::msg::SensorSet msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::tku_msgs::msg::SensorSet>()
{
  return tku_msgs::msg::builder::Init_SensorSet_sensor_p();
}

}  // namespace tku_msgs

#endif  // TKU_MSGS__MSG__DETAIL__SENSOR_SET__BUILDER_HPP_
