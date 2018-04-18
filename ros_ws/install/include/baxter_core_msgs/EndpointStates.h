// Generated by gencpp from file baxter_core_msgs/EndpointStates.msg
// DO NOT EDIT!


#ifndef BAXTER_CORE_MSGS_MESSAGE_ENDPOINTSTATES_H
#define BAXTER_CORE_MSGS_MESSAGE_ENDPOINTSTATES_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <baxter_core_msgs/EndpointState.h>

namespace baxter_core_msgs
{
template <class ContainerAllocator>
struct EndpointStates_
{
  typedef EndpointStates_<ContainerAllocator> Type;

  EndpointStates_()
    : names()
    , states()  {
    }
  EndpointStates_(const ContainerAllocator& _alloc)
    : names(_alloc)
    , states(_alloc)  {
  (void)_alloc;
    }



   typedef std::vector<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > , typename ContainerAllocator::template rebind<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::other >  _names_type;
  _names_type names;

   typedef std::vector< ::baxter_core_msgs::EndpointState_<ContainerAllocator> , typename ContainerAllocator::template rebind< ::baxter_core_msgs::EndpointState_<ContainerAllocator> >::other >  _states_type;
  _states_type states;




  typedef boost::shared_ptr< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> const> ConstPtr;

}; // struct EndpointStates_

typedef ::baxter_core_msgs::EndpointStates_<std::allocator<void> > EndpointStates;

typedef boost::shared_ptr< ::baxter_core_msgs::EndpointStates > EndpointStatesPtr;
typedef boost::shared_ptr< ::baxter_core_msgs::EndpointStates const> EndpointStatesConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::baxter_core_msgs::EndpointStates_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace baxter_core_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'sensor_msgs': ['/opt/ros/kinetic/share/sensor_msgs/cmake/../msg'], 'geometry_msgs': ['/opt/ros/kinetic/share/geometry_msgs/cmake/../msg'], 'baxter_core_msgs': ['/home/parallels/ros_ws/src/baxter_common/baxter_core_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a0ca50a066809a5f065f39f37aa028fb";
  }

  static const char* value(const ::baxter_core_msgs::EndpointStates_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa0ca50a066809a5fULL;
  static const uint64_t static_value2 = 0x065f39f37aa028fbULL;
};

template<class ContainerAllocator>
struct DataType< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
{
  static const char* value()
  {
    return "baxter_core_msgs/EndpointStates";
  }

  static const char* value(const ::baxter_core_msgs::EndpointStates_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string[] names\n\
EndpointState[] states\n\
\n\
\n\
================================================================================\n\
MSG: baxter_core_msgs/EndpointState\n\
Header header\n\
geometry_msgs/Pose   pose\n\
geometry_msgs/Twist  twist\n\
geometry_msgs/Wrench wrench\n\
\n\
================================================================================\n\
MSG: std_msgs/Header\n\
# Standard metadata for higher-level stamped data types.\n\
# This is generally used to communicate timestamped data \n\
# in a particular coordinate frame.\n\
# \n\
# sequence ID: consecutively increasing ID \n\
uint32 seq\n\
#Two-integer timestamp that is expressed as:\n\
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n\
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n\
# time-handling sugar is provided by the client library\n\
time stamp\n\
#Frame this data is associated with\n\
# 0: no frame\n\
# 1: global frame\n\
string frame_id\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Pose\n\
# A representation of pose in free space, composed of position and orientation. \n\
Point position\n\
Quaternion orientation\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Point\n\
# This contains the position of a point in free space\n\
float64 x\n\
float64 y\n\
float64 z\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Quaternion\n\
# This represents an orientation in free space in quaternion form.\n\
\n\
float64 x\n\
float64 y\n\
float64 z\n\
float64 w\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Twist\n\
# This expresses velocity in free space broken into its linear and angular parts.\n\
Vector3  linear\n\
Vector3  angular\n\
\n\
================================================================================\n\
MSG: geometry_msgs/Vector3\n\
# This represents a vector in free space. \n\
# It is only meant to represent a direction. Therefore, it does not\n\
# make sense to apply a translation to it (e.g., when applying a \n\
# generic rigid transformation to a Vector3, tf2 will only apply the\n\
# rotation). If you want your data to be translatable too, use the\n\
# geometry_msgs/Point message instead.\n\
\n\
float64 x\n\
float64 y\n\
float64 z\n\
================================================================================\n\
MSG: geometry_msgs/Wrench\n\
# This represents force in free space, separated into\n\
# its linear and angular parts.\n\
Vector3  force\n\
Vector3  torque\n\
";
  }

  static const char* value(const ::baxter_core_msgs::EndpointStates_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.names);
      stream.next(m.states);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct EndpointStates_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::baxter_core_msgs::EndpointStates_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::baxter_core_msgs::EndpointStates_<ContainerAllocator>& v)
  {
    s << indent << "names[]" << std::endl;
    for (size_t i = 0; i < v.names.size(); ++i)
    {
      s << indent << "  names[" << i << "]: ";
      Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.names[i]);
    }
    s << indent << "states[]" << std::endl;
    for (size_t i = 0; i < v.states.size(); ++i)
    {
      s << indent << "  states[" << i << "]: ";
      s << std::endl;
      s << indent;
      Printer< ::baxter_core_msgs::EndpointState_<ContainerAllocator> >::stream(s, indent + "    ", v.states[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // BAXTER_CORE_MSGS_MESSAGE_ENDPOINTSTATES_H
