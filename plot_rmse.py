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

# ★ 最適点を強調（文字なし）
best_tau = taus[rmses.index(min(rmses))]
best_rmse = min(rmses)

plt.scatter([best_tau], [best_rmse], s=120, color='red', zorder=3)

plt.xlabel("tau")
plt.ylabel("RMSE")
plt.title("RMSE vs tau")

plt.grid()

# 保存
output_path = "data/rmse_vs_tau.png"
plt.savefig(output_path)