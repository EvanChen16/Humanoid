// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from tku_msgs:srv/SetString.idl
// generated code does not contain a copyright notice

#ifndef TKU_MSGS__SRV__DETAIL__SET_STRING__BUILDER_HPP_
#define TKU_MSGS__SRV__DETAIL__SET_STRING__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "tku_msgs/srv/detail/set_string__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace tku_msgs
{

namespace srv
{

namespace builder
{

class Init_SetString_Request_data
{
public:
  Init_SetString_Request_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::tku_msgs::srv::SetString_Request data(::tku_msgs::srv::SetString_Request::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tku_msgs::srv::SetString_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::tku_msgs::srv::SetString_Request>()
{
  return tku_msgs::srv::builder::Init_SetString_Request_data();
}

}  // namespace tku_msgs


namespace tku_msgs
{

namespace srv
{

namespace builder
{

class Init_SetString_Response_data
{
public:
  Init_SetString_Response_data()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::tku_msgs::srv::SetString_Response data(::tku_msgs::srv::SetString_Response::_data_type arg)
  {
    msg_.data = std::move(arg);
    return std::move(msg_);
  }

private:
  ::tku_msgs::srv::SetString_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::tku_msgs::srv::SetString_Response>()
{
  return tku_msgs::srv::builder::Init_SetString_Response_data();
}

}  // namespace tku_msgs

#endif  // TKU_MSGS__SRV__DETAIL__SET_STRING__BUILDER_HPP_
