// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tku_msgs:msg/SensorSet.idl
// generated code does not contain a copyright notice

#ifndef TKU_MSGS__MSG__DETAIL__SENSOR_SET__STRUCT_HPP_
#define TKU_MSGS__MSG__DETAIL__SENSOR_SET__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tku_msgs__msg__SensorSet __attribute__((deprecated))
#else
# define DEPRECATED__tku_msgs__msg__SensorSet __declspec(deprecated)
#endif

namespace tku_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SensorSet_
{
  using Type = SensorSet_<ContainerAllocator>;

  explicit SensorSet_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sensor_p = 0l;
      this->sensor_i = 0l;
      this->sensor_d = 0l;
      this->roll = 0l;
      this->pitch = 0l;
      this->yaw = 0l;
      this->sup_f = 0l;
      this->nsup_f = 0l;
      this->sensor_modeset = 0l;
    }
  }

  explicit SensorSet_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->sensor_p = 0l;
      this->sensor_i = 0l;
      this->sensor_d = 0l;
      this->roll = 0l;
      this->pitch = 0l;
      this->yaw = 0l;
      this->sup_f = 0l;
      this->nsup_f = 0l;
      this->sensor_modeset = 0l;
    }
  }

  // field types and members
  using _sensor_p_type =
    int32_t;
  _sensor_p_type sensor_p;
  using _sensor_i_type =
    int32_t;
  _sensor_i_type sensor_i;
  using _sensor_d_type =
    int32_t;
  _sensor_d_type sensor_d;
  using _roll_type =
    int32_t;
  _roll_type roll;
  using _pitch_type =
    int32_t;
  _pitch_type pitch;
  using _yaw_type =
    int32_t;
  _yaw_type yaw;
  using _sup_f_type =
    int32_t;
  _sup_f_type sup_f;
  using _nsup_f_type =
    int32_t;
  _nsup_f_type nsup_f;
  using _sensor_modeset_type =
    int32_t;
  _sensor_modeset_type sensor_modeset;

  // setters for named parameter idiom
  Type & set__sensor_p(
    const int32_t & _arg)
  {
    this->sensor_p = _arg;
    return *this;
  }
  Type & set__sensor_i(
    const int32_t & _arg)
  {
    this->sensor_i = _arg;
    return *this;
  }
  Type & set__sensor_d(
    const int32_t & _arg)
  {
    this->sensor_d = _arg;
    return *this;
  }
  Type & set__roll(
    const int32_t & _arg)
  {
    this->roll = _arg;
    return *this;
  }
  Type & set__pitch(
    const int32_t & _arg)
  {
    this->pitch = _arg;
    return *this;
  }
  Type & set__yaw(
    const int32_t & _arg)
  {
    this->yaw = _arg;
    return *this;
  }
  Type & set__sup_f(
    const int32_t & _arg)
  {
    this->sup_f = _arg;
    return *this;
  }
  Type & set__nsup_f(
    const int32_t & _arg)
  {
    this->nsup_f = _arg;
    return *this;
  }
  Type & set__sensor_modeset(
    const int32_t & _arg)
  {
    this->sensor_modeset = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tku_msgs::msg::SensorSet_<ContainerAllocator> *;
  using ConstRawPtr =
    const tku_msgs::msg::SensorSet_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tku_msgs::msg::SensorSet_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tku_msgs::msg::SensorSet_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tku_msgs__msg__SensorSet
    std::shared_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tku_msgs__msg__SensorSet
    std::shared_ptr<tku_msgs::msg::SensorSet_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SensorSet_ & other) const
  {
    if (this->sensor_p != other.sensor_p) {
      return false;
    }
    if (this->sensor_i != other.sensor_i) {
      return false;
    }
    if (this->sensor_d != other.sensor_d) {
      return false;
    }
    if (this->roll != other.roll) {
      return false;
    }
    if (this->pitch != other.pitch) {
      return false;
    }
    if (this->yaw != other.yaw) {
      return false;
    }
    if (this->sup_f != other.sup_f) {
      return false;
    }
    if (this->nsup_f != other.nsup_f) {
      return false;
    }
    if (this->sensor_modeset != other.sensor_modeset) {
      return false;
    }
    return true;
  }
  bool operator!=(const SensorSet_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SensorSet_

// alias to use template instance with default allocator
using SensorSet =
  tku_msgs::msg::SensorSet_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace tku_msgs

#endif  // TKU_MSGS__MSG__DETAIL__SENSOR_SET__STRUCT_HPP_
