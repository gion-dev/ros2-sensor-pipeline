import subprocess
import time
import csv
import math
import os
import signal

TAUS = [0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]
RESULT_CSV = "data/experiment_results.csv"

def calculate_rmse(csv_path):
    raw_data = []
    filtered_data = []

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue  # ← 不正行スキップ

            try:
                raw = float(row[0])
                filtered = float(row[1])
            except ValueError:
                continue  # ← 壊れた行スキップ

            raw_data.append(raw)
            filtered_data.append(filtered)

    if len(raw_data) == 0:
        return float("nan")

    error = [raw_data[i] - filtered_data[i] for i in range(len(raw_data))]
    return math.sqrt(sum(e**2 for e in error) / len(error))


def run_ros(tau):
    print(f"\n=== Running tau={tau} ===")

    proc = subprocess.Popen([
        "ros2", "launch", "sensor_pipeline_launch", "pipeline.launch.py",
        f"tau:={tau}"
    ])

    # データ収集
    time.sleep(5)

    # Ctrl+C相当で終了（重要）
    proc.send_signal(signal.SIGINT)
    time.sleep(2)
    proc.wait()

    time.sleep(1)


def main():
    os.makedirs("data", exist_ok=True)

    with open(RESULT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tau", "rmse"])

        for tau in TAUS:
            run_ros(tau)

            # ★ tauごとのCSVを読む（ここ重要）
            csv_path = f"data/sample_tau_{tau}.csv"

            if not os.path.exists(csv_path):
                print(f"CSV not found: {csv_path}")
                continue

            rmse = calculate_rmse(csv_path)

            print(f"tau={tau} → RMSE={rmse:.3f}")

            writer.writerow([tau, rmse])


if __name__ == "__main__":
    main()