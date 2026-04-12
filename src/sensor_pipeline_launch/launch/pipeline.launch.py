from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='sensor_pipeline_cpp',
            executable='sensor_node',
            output='screen'
        ),

        Node(
            package='sensor_pipeline_cpp',
            executable='filter_node',
            output='screen'
        ),

        Node(
            package='sensor_pipeline_py',
            executable='visualize_node',
            output='screen'
        ),
    ])