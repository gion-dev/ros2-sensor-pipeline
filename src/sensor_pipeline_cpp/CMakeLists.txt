cmake_minimum_required(VERSION 3.8)
project(sensor_pipeline_cpp)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(sensor_node src/sensor_node.cpp)
ament_target_dependencies(sensor_node rclcpp std_msgs)

add_executable(filter_node src/filter_node.cpp)
ament_target_dependencies(filter_node rclcpp std_msgs)

install(TARGETS
  sensor_node
  filter_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()