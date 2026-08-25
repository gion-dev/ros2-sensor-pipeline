import subprocess
import sys

def run_command(cmd):
    # 指定したコマンドを実行
    print(f"\n>>> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    # コマンドが失敗した場合は処理を中断
    if result.returncode != 0:
        print("❌ Error occurred. Stopping.")
        sys.exit(1)


def main():
    print("=== ROS2 Sensor Pipeline Auto Run ===")

    # EMAの時定数を変更しながら実験を実行
    run_command(["python3", "sweep_tau.py"])

    # 実験結果からRMSEグラフを生成
    run_command(["python3", "plot_rmse.py"])

    print("\n=== All Done ===")
    print("Check 'data/' directory for results.")


if __name__ == "__main__":
    main()