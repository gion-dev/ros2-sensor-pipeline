import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import os
import csv

MAX_POINTS = 200  # 表示する最大点数

class VisualizeNode(Node):
    def __init__(self):
        super().__init__('visualize_node')

        self.sub_raw = self.create_subscription(
            Float64,
            'sensor/raw',
            self.callback_raw,
            10
        )

        self.sub_filtered = self.create_subscription(
            Float64,
            'sensor/filtered',
            self.callback_filtered,
            10
        )

        self.raw_data = []
        self.filtered_data = []
        self.step = 0

        # 保存先
        self.base_dir = os.path.expanduser('~/work/ros2-sensor-pipeline/data')
        os.makedirs(self.base_dir, exist_ok=True)

        self.get_logger().info("Visualize node started")

    def callback_raw(self, msg):
        self.raw_data.append(msg.data)
        if len(self.raw_data) > MAX_POINTS:
            self.raw_data.pop(0)

    def callback_filtered(self, msg):
        self.filtered_data.append(msg.data)
        if len(self.filtered_data) > MAX_POINTS:
            self.filtered_data.pop(0)

        self.step += 1

        # 一定間隔で保存
        if self.step % 50 == 0:
            self.save_plot()
            self.save_csv()

    def save_plot(self):
        try:
            plt.figure()

            # raw
            plt.plot(
                self.raw_data,
                label='raw',
                linestyle='-',
                alpha=0.8
            )

            # filtered
            plt.plot(
                self.filtered_data,
                label='filtered',
                linewidth=2
            )

            plt.title("Sensor Data")
            plt.xlabel("Step")
            plt.ylabel("Value")
            plt.legend()
            plt.grid()

            output_path = os.path.join(self.base_dir, 'result.png')
            plt.savefig(output_path)
            plt.close()

            self.get_logger().info(f"Saved plot: {output_path}")

        except Exception as e:
            self.get_logger().warn(f"Plot save failed: {e}")

    def save_csv(self):
        try:
            output_path = os.path.join(self.base_dir, 'sample.csv')

            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['raw', 'filtered'])

                for r, f_val in zip(self.raw_data, self.filtered_data):
                    writer.writerow([r, f_val])

            self.get_logger().info(f"Saved CSV: {output_path}")

        except Exception as e:
            self.get_logger().warn(f"CSV save failed: {e}")

    def destroy_node(self):
        # 終了時に最後の保存（ここが超重要）
        self.get_logger().info("Saving final output before shutdown...")
        self.save_plot()
        self.save_csv()
        super().destroy_node()


def main():
    rclpy.init()
    node = VisualizeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # ここで確実に保存
    node.destroy_node()
    rclpy.shutdown()