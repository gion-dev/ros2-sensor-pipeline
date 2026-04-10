#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import matplotlib.pyplot as plt
import csv
import numpy as np


class VisualizeNode(Node):

    def __init__(self):
        super().__init__('visualize_node')

        self.raw_data = []
        self.filtered_data = []

        # CSV準備
        self.csv_file = open('data/sample.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        self.csv_writer.writerow(['raw', 'filtered'])

        # Subscriber
        self.create_subscription(
            Float64,
            '/sensor/raw',
            self.raw_callback,
            10)

        self.create_subscription(
            Float64,
            '/sensor/filtered',
            self.filtered_callback,
            10)

        # タイマー（1秒ごとに処理）
        self.timer = self.create_timer(1.0, self.process)

        self.get_logger().info("Visualize node started")

        plt.ion()

    def raw_callback(self, msg):
        self.raw_data.append(msg.data)

    def filtered_callback(self, msg):
        self.filtered_data.append(msg.data)

    def process(self):
        print("process called")
        print(f"raw: {len(self.raw_data)}, filtered: {len(self.filtered_data)}")

        min_len = min(len(self.raw_data), len(self.filtered_data))

        if min_len < 1:
            return

        # --- CSV保存 ---
        for i in range(min_len):
            self.csv_writer.writerow([
                self.raw_data[i],
                self.filtered_data[i]
            ])
        self.csv_file.flush()

        # --- RMSE計算 ---
        raw = np.array(self.raw_data[:min_len])
        filtered = np.array(self.filtered_data[:min_len])

        rmse = np.sqrt(np.mean((raw - filtered) ** 2))
        print(f"RMSE: {rmse:.4f}")

        # --- グラフ描画 ---
        plt.clf()
        plt.plot(raw, label='Raw')
        plt.plot(filtered, label='Filtered')
        plt.legend()
        plt.draw()
        plt.pause(0.01)

        # --- 画像保存（上書き） ---
        plt.savefig("data/result.png")


def main(args=None):
    rclpy.init(args=args)
    node = VisualizeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Shutting down visualize node...")
    finally:
        node.csv_file.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()