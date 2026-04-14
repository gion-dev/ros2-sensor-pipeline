from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    tau = LaunchConfiguration('tau')

    return LaunchDescription([

        # ===== 引数宣言 =====
        DeclareLaunchArgument(
            'tau',
            default_value='0.5',
            description='Time constant for EMA filter'
        ),

        Node(
            package='sensor_pipeline_cpp',
            executable='sensor_node',
            name='sensor_node'
        ),

        Node(
            package='sensor_pipeline_cpp',
            executable='filter_node',
            name='filter_node',
            parameters=[{
                'tau': tau
            }]
        ),

        Node(
            package='sensor_pipeline_py',
            executable='visualize_node',
            name='visualize_node',
            parameters=[{
                'tau': tau
            }]
        ),
    ])