import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import csv
import os
import math

MAX_POINTS = 200

class VisualizeNode(Node):
    def __init__(self):
        super().__init__('visualize_node')

        self.raw_data = []
        self.filtered_data = []
        self.is_saving = False

        # ===== パス設定 =====
        self.base_path = os.path.expanduser("~/work/ros2-sensor-pipeline/data")
        os.makedirs(self.base_path, exist_ok=True)

        self.tmp_path = os.path.join(self.base_path, "result_tmp.png")
        self.final_path = os.path.join(self.base_path, "result.png")
        self.csv_path = os.path.join(self.base_path, "sample.csv")

        # ===== 起動時にtmp削除 =====
        if os.path.exists(self.tmp_path):
            try:
                os.remove(self.tmp_path)
                self.get_logger().info("Removed leftover tmp file")
            except Exception as e:
                self.get_logger().warn(f"Failed to remove tmp file: {e}")

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

    def callback_raw(self, msg):
        self.raw_data.append(msg.data)
        if len(self.raw_data) > MAX_POINTS:
            self.raw_data.pop(0)

    def callback_filtered(self, msg):
        self.filtered_data.append(msg.data)
        if len(self.filtered_data) > MAX_POINTS:
            self.filtered_data.pop(0)

        if len(self.raw_data) == len(self.filtered_data):
            if not self.is_saving:
                self.save_all()

    def save_all(self):
        self.is_saving = True

        try:
            # ===== データ準備 =====
            x = list(range(len(self.raw_data)))
            error = [r - f for r, f in zip(self.raw_data, self.filtered_data)]

            mse = sum(e**2 for e in error) / len(error)
            rmse = math.sqrt(mse)

            # ===== CSV保存 =====
            with open(self.csv_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["step", "raw", "filtered", "error"])
                for i in range(len(x)):
                    writer.writerow([i, self.raw_data[i], self.filtered_data[i], error[i]])

            # ===== グラフ描画 =====
            plt.figure(figsize=(10, 6))

            # 上の線
            plt.subplot(2, 1, 1)
            plt.plot(x, self.raw_data, alpha=0.9, label="raw")
            plt.plot(x, self.filtered_data, label="filtered", linewidth=2)
            plt.title(f"Sensor Data (RMSE={rmse:.3f})")
            plt.legend()
            plt.grid()

            # 下の線
            plt.subplot(2, 1, 2)
            plt.plot(x, error, color="red",  alpha=0.7, label="error")
            plt.legend()
            plt.grid()

            plt.tight_layout()

            # ===== tmpに保存 =====
            plt.savefig(self.tmp_path)
            plt.close()

            # ===== 完了後に置き換え =====
            os.replace(self.tmp_path, self.final_path)

            self.get_logger().info(f"Saved plot & csv (RMSE={rmse:.3f})")

        finally:
            self.is_saving = False

            # ===== finallyでもtmp削除 =====
            if os.path.exists(self.tmp_path):
                try:
                    os.remove(self.tmp_path)
                except:
                    pass

def main():
    rclpy.init()
    node = VisualizeNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down safely...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()