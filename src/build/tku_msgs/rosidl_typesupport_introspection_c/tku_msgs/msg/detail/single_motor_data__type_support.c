// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from tku_msgs:msg/SingleMotorData.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "tku_msgs/msg/detail/single_motor_data__rosidl_typesupport_introspection_c.h"
#include "tku_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "tku_msgs/msg/detail/single_motor_data__functions.h"
#include "tku_msgs/msg/detail/single_motor_data__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  tku_msgs__msg__SingleMotorData__init(message_memory);
}

void tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_fini_function(void * message_memory)
{
  tku_msgs__msg__SingleMotorData__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_member_array[3] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(tku_msgs__msg__SingleMotorData, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "position",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(tku_msgs__msg__SingleMotorData, position),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "speed",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT16,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(tku_msgs__msg__SingleMotorData, speed),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_members = {
  "tku_msgs__msg",  // message namespace
  "SingleMotorData",  // message name
  3,  // number of fields
  sizeof(tku_msgs__msg__SingleMotorData),
  tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_member_array,  // message members
  tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_init_function,  // function to initialize message memory (memory has to be allocated)
  tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_type_support_handle = {
  0,
  &tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_tku_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, tku_msgs, msg, SingleMotorData)() {
  if (!tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_type_support_handle.typesupport_identifier) {
    tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &tku_msgs__msg__SingleMotorData__rosidl_typesupport_introspection_c__SingleMotorData_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
