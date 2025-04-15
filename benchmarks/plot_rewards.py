import matplotlib.pyplot as plt
import csv

episodes = []
totals = []
agent_0 = []
agent_1 = []

with open("benchmarks/results/rewards.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        episodes.append(int(row["episode"]))
        totals.append(float(row["total_reward"]))
        agent_0.append(float(row["agent_0"]))
        agent_1.append(float(row["agent_1"]))

plt.plot(episodes, totals, label="Total Reward")
plt.plot(episodes, agent_0, label="Agent 0")
plt.plot(episodes, agent_1, label="Agent 1")
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("VISTA-MARL Reward Curve")
plt.legend()
plt.grid(True)
plt.savefig("benchmarks/results/reward_plot.png")
plt.show()
