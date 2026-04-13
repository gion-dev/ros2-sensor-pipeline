#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os
import csv

MAX_POINTS = 500  # 表示する最大データ数

class VisualizeNode(Node):
    def __init__(self):
        super().__init__('visualize_node')

        # ===== Subscriber =====
        self.sub_raw = self.create_subscription(
            Float64,
            '/sensor/raw',
            self.callback_raw,
            10
        )

        self.sub_filtered = self.create_subscription(
            Float64,
            '/sensor/filtered',
            self.callback_filtered,
            10
        )

        # ===== データ保持 =====
        self.raw_data = []
        self.filtered_data = []
        self.time_data = []
        self.t = 0

        # ===== 出力先 =====
        self.output_dir = os.path.expanduser('~/work/ros2-sensor-pipeline/data')
        os.makedirs(self.output_dir, exist_ok=True)

        self.png_path = os.path.join(self.output_dir, 'result.png')
        self.csv_path = os.path.join(self.output_dir, 'sample.csv')

        self.get_logger().info(f'Output dir: {self.output_dir}')

    def callback_raw(self, msg):
        self.raw_data.append(msg.data)

    def callback_filtered(self, msg):
        self.filtered_data.append(msg.data)

        # 時間更新
        self.t += 1
        self.time_data.append(self.t)

        # データ長制限
        if len(self.raw_data) > MAX_POINTS:
            self.raw_data.pop(0)
        if len(self.filtered_data) > MAX_POINTS:
            self.filtered_data.pop(0)
            self.time_data.pop(0)

        # 描画
        self.save_plot()

    def save_plot(self):
        try:
            plt.clf()

            # raw（薄い線）
            plt.plot(self.time_data, self.raw_data,
                     label='raw',
                     alpha=0.7)

            # filtered（強調）
            plt.plot(self.time_data, self.filtered_data,
                     label='filtered',
                     linewidth=2)

            plt.legend()
            plt.xlabel('time')
            plt.ylabel('value')
            plt.title('Sensor Data (Raw vs Filtered)')

            plt.savefig(self.png_path)

            # CSV保存
            with open(self.csv_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['time', 'raw', 'filtered'])

                for i in range(len(self.filtered_data)):
                    raw = self.raw_data[i] if i < len(self.raw_data) else ''
                    writer.writerow([self.time_data[i], raw, self.filtered_data[i]])

            self.get_logger().info('Saved plot & csv')

        except Exception as e:
            self.get_logger().error(f'Plot error: {e}')

def main():
    rclpy.init()
    node = VisualizeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down safely...')
    finally:
        if rclpy.ok():
            rclpy.shutdown()