// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from tku_msgs:msg/LabelModelObjectList.idl
// generated code does not contain a copyright notice

#ifndef TKU_MSGS__MSG__DETAIL__LABEL_MODEL_OBJECT_LIST__STRUCT_HPP_
#define TKU_MSGS__MSG__DETAIL__LABEL_MODEL_OBJECT_LIST__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__tku_msgs__msg__LabelModelObjectList __attribute__((deprecated))
#else
# define DEPRECATED__tku_msgs__msg__LabelModelObjectList __declspec(deprecated)
#endif

namespace tku_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct LabelModelObjectList_
{
  using Type = LabelModelObjectList_<ContainerAllocator>;

  explicit LabelModelObjectList_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
  }

  explicit LabelModelObjectList_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_init;
    (void)_alloc;
  }

  // field types and members
  using _labelmodel_type =
    std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>>;
  _labelmodel_type labelmodel;

  // setters for named parameter idiom
  Type & set__labelmodel(
    const std::vector<uint8_t, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<uint8_t>> & _arg)
  {
    this->labelmodel = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    tku_msgs::msg::LabelModelObjectList_<ContainerAllocator> *;
  using ConstRawPtr =
    const tku_msgs::msg::LabelModelObjectList_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      tku_msgs::msg::LabelModelObjectList_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      tku_msgs::msg::LabelModelObjectList_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__tku_msgs__msg__LabelModelObjectList
    std::shared_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__tku_msgs__msg__LabelModelObjectList
    std::shared_ptr<tku_msgs::msg::LabelModelObjectList_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const LabelModelObjectList_ & other) const
  {
    if (this->labelmodel != other.labelmodel) {
      return false;
    }
    return true;
  }
  bool operator!=(const LabelModelObjectList_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct LabelModelObjectList_

// alias to use template instance with default allocator
using LabelModelObjectList =
  tku_msgs::msg::LabelModelObjectList_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace tku_msgs

#endif  // TKU_MSGS__MSG__DETAIL__LABEL_MODEL_OBJECT_LIST__STRUCT_HPP_
