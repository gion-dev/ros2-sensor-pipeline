from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([

        Node(
            package='sensor_pipeline_cpp',
            executable='sensor_node',
            parameters=[{'noise': 0.3}]
        ),

        Node(
            package='sensor_pipeline_cpp',
            executable='filter_node',
            parameters=[{'alpha': 0.2}]
        ),

        Node(
            package='sensor_pipeline_py',
            executable='visualize_node',
            output='screen'
        ),
    ])