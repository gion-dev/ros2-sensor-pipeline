import csv
import matplotlib.pyplot as plt

CSV_PATH = "data/experiment_results.csv"

taus = []
rmses = []

# CSV読み込み
with open(CSV_PATH, "r") as f:
    reader = csv.reader(f)
    next(reader)  # ヘッダスキップ

    for row in reader:
        tau = float(row[0])
        rmse = float(row[1])
        taus.append(tau)
        rmses.append(rmse)

# グラフ描画
plt.figure()
plt.plot(taus, rmses, marker='o')

plt.xlabel("tau")
plt.ylabel("RMSE")
plt.title("RMSE vs tau")

plt.grid()

# 保存
output_path = "data/rmse_vs_tau.png"
plt.savefig(output_path)