import subprocess
import time
import csv
import math
import os
import signal

# 評価対象とするEMAの時定数
TAUS = [0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3]

# 結果の保存先
RESULT_CSV = "data/experiment_results.csv"

def calculate_rmse(csv_path):
    raw_data = []
    filtered_data = []

    # CSVから生データとフィルタリング後のデータを読み込み
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            if len(row) < 2:
                continue  # 不正な行をスキップ

            try:
                raw = float(row[1])
                filtered = float(row[2])
            except ValueError:
                continue  # 数値に変換できない行をスキップ

            raw_data.append(raw)
            filtered_data.append(filtered)

     # 有効なデータがない場合はNaNを返す
    if len(raw_data) == 0:
        return float("nan")

    # 生データとフィルタリング後のデータからRMSEを算出（ここでのerrorは誤差算出として使用）
    error = [raw_data[i] - filtered_data[i] for i in range(len(raw_data))]
    return math.sqrt(sum(e**2 for e in error) / len(error))


def run_ros(tau):
    print(f"\n=== Running tau={tau} ===")

    # 指定したtauでROS起動
    proc = subprocess.Popen([
        "ros2", "launch", "sensor_pipeline_launch", "pipeline.launch.py",
        f"tau:={tau}"
    ])

    # データ収集時間を確保
    time.sleep(5)

    # Ctrl+C相当で終了
    proc.send_signal(signal.SIGINT)
    time.sleep(2)
    proc.wait()

    time.sleep(1)


def main():
    # データ保存先ディレクトリを作成
    os.makedirs("data", exist_ok=True)

    # 実験結果CSVを初期化
    with open(RESULT_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tau", "rmse"])
        
        # tauごとにROS2パイプラインを実行
        for tau in TAUS:
            run_ros(tau)

            # tauごとのCSVを読み込む
            csv_path = f"data/sample_tau_{tau}.csv"

            if not os.path.exists(csv_path):
                print(f"CSV not found: {csv_path}")
                continue

            # RMSEを算出
            rmse = calculate_rmse(csv_path)

            print(f"tau={tau} → RMSE={rmse:.3f}")

             # tauとRMSEの結果を保存
            writer.writerow([tau, rmse])


if __name__ == "__main__":
    main()