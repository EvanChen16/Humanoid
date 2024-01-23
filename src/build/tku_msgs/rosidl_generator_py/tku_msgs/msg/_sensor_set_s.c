// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from tku_msgs:msg/SensorSet.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "tku_msgs/msg/detail/sensor_set__struct.h"
#include "tku_msgs/msg/detail/sensor_set__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool tku_msgs__msg__sensor_set__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[35];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("tku_msgs.msg._sensor_set.SensorSet", full_classname_dest, 34) == 0);
  }
  tku_msgs__msg__SensorSet * ros_message = _ros_message;
  {  // sensor_p
    PyObject * field = PyObject_GetAttrString(_pymsg, "sensor_p");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sensor_p = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // sensor_i
    PyObject * field = PyObject_GetAttrString(_pymsg, "sensor_i");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sensor_i = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // sensor_d
    PyObject * field = PyObject_GetAttrString(_pymsg, "sensor_d");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sensor_d = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // roll
    PyObject * field = PyObject_GetAttrString(_pymsg, "roll");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->roll = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // pitch
    PyObject * field = PyObject_GetAttrString(_pymsg, "pitch");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->pitch = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // yaw
    PyObject * field = PyObject_GetAttrString(_pymsg, "yaw");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->yaw = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // sup_f
    PyObject * field = PyObject_GetAttrString(_pymsg, "sup_f");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sup_f = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // nsup_f
    PyObject * field = PyObject_GetAttrString(_pymsg, "nsup_f");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->nsup_f = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }
  {  // sensor_modeset
    PyObject * field = PyObject_GetAttrString(_pymsg, "sensor_modeset");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->sensor_modeset = (int32_t)PyLong_AsLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * tku_msgs__msg__sensor_set__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of SensorSet */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("tku_msgs.msg._sensor_set");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "SensorSet");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  tku_msgs__msg__SensorSet * ros_message = (tku_msgs__msg__SensorSet *)raw_ros_message;
  {  // sensor_p
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->sensor_p);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sensor_p", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // sensor_i
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->sensor_i);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sensor_i", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // sensor_d
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->sensor_d);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sensor_d", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // roll
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->roll);
    {
      int rc = PyObject_SetAttrString(_pymessage, "roll", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // pitch
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->pitch);
    {
      int rc = PyObject_SetAttrString(_pymessage, "pitch", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // yaw
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->yaw);
    {
      int rc = PyObject_SetAttrString(_pymessage, "yaw", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // sup_f
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->sup_f);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sup_f", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // nsup_f
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->nsup_f);
    {
      int rc = PyObject_SetAttrString(_pymessage, "nsup_f", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // sensor_modeset
    PyObject * field = NULL;
    field = PyLong_FromLong(ros_message->sensor_modeset);
    {
      int rc = PyObject_SetAttrString(_pymessage, "sensor_modeset", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
