import subprocess
import sys

def run_command(cmd):
    print(f"\n>>> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("❌ Error occurred. Stopping.")
        sys.exit(1)


def main():
    print("=== ROS2 Sensor Pipeline Auto Run ===")

    # ① 実験実行
    run_command(["python3", "sweep_tau.py"])

    # ② グラフ生成
    run_command(["python3", "plot_rmse.py"])

    print("\n=== All Done ===")
    print("Check 'data/' directory for results.")


if __name__ == "__main__":
    main()