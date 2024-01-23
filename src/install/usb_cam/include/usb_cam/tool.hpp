// #ifndef TOOL_H
// #define TOOL_H

// #include <ament_index_cpp/get_package_share_directory.hpp>
// #include <rclcpp/rclcpp.hpp>
// #include <sys/time.h>
// #include <fstream>
// #include <sstream>
// #include <cmath>
// #include <vector>
// #include <iostream>
// #include <string>

// class Tool
// {
//     public:
//         Tool();
//         ~Tool();
//         std::string getPackagePath(std::string package_name);
//         float readvalue(std::fstream &fin, std::string title, int mode);
//     public:
//         std::string parameterPath;
//     private:
//         std::string packagePath;
// };

// class ToolInstance : public Tool
// {
//     public:
//         ToolInstance() : Tool() {}
//         ~ToolInstance() {}
//         static ToolInstance* getInstance();
//     private:
//         static ToolInstance *m_pInstance;
// };

// #endif // TOOL_H