from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    # Launch引数からEMAフィルタの時定数を取得
    tau = LaunchConfiguration('tau')

    return LaunchDescription([

        # Launch引数の宣言
        DeclareLaunchArgument(
            'tau',
            default_value='0.5',
            description='Time constant for EMA filter'
        ),

        # 疑似センサーデータを生成・配信するノード
        Node(
            package='sensor_pipeline_cpp',
            executable='sensor_node',
            name='sensor_node'
        ),

        # 疑似センサーデータをEMAフィルタでフィルタリングするノード
        Node(
            package='sensor_pipeline_cpp',
            executable='filter_node',
            name='filter_node',
            parameters=[{
                'tau': tau
            }]
        ),

        # フィルタリング結果を可視化するノード
        Node(
            package='sensor_pipeline_py',
            executable='visualize_node',
            name='visualize_node',
            parameters=[{
                'tau': tau
            }]
        ),
    ])