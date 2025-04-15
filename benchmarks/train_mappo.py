

# import random
# from vista_env.core.env import VISTAEnv

# def greedy_action(pos, resources, grid_size):
#     if not resources:
#         return 0  # Stay
#     nearest = min(resources, key=lambda r: abs(r[0] - pos[0]) + abs(r[1] - pos[1]))
#     dr, dc = nearest[0] - pos[0], nearest[1] - pos[1]
#     if abs(dr) > abs(dc):
#         return 1 if dr < 0 else 2  # up/down
#     elif abs(dc) > 0:
#         return 3 if dc < 0 else 4  # left/right
#     return 0  # Already on resource

# config = {
#     "grid_size": 10,
#     "max_steps": 50,
#     "num_agents": 2,
#     "roles": ["gatherer", "defender"]
# }

# env = VISTAEnv(config)
# obs = env.reset()
# done = {agent_id: False for agent_id in obs}

# print("👾 Starting VISTA-MARL greedy agent demo...\n")

# while not all(done.values()):
#     actions = {
#         agent_id: greedy_action(env.agents[agent_id], env.resources, env.grid_size)
#         for agent_id in obs
#     }
#     obs, rewards, done, _ = env.step(actions)
#     env.render()
#     print(rewards)
#     print("-" * 40)

# print("✅ Episode finished.\n")


import os
import csv
import random
from vista_env.core.env import VISTAEnv

def greedy_action(pos, resources, grid_size):
    if not resources:
        return 0  # Stay
    nearest = min(resources, key=lambda r: abs(r[0] - pos[0]) + abs(r[1] - pos[1]))
    dr, dc = nearest[0] - pos[0], nearest[1] - pos[1]
    if abs(dr) > abs(dc):
        return 1 if dr < 0 else 2  # up/down
    elif abs(dc) > 0:
        return 3 if dc < 0 else 4  # left/right
    return 0  # Already on resource

config = {
    "grid_size": 10,
    "max_steps": 50,
    "num_agents": 2,
    "roles": ["gatherer", "defender"]
}

env = VISTAEnv(config)

# Ensure results directory exists
os.makedirs("benchmarks/results", exist_ok=True)
csv_file = "benchmarks/results/rewards.csv"

with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["episode", "total_reward", "agent_0", "agent_1"])

    print("👾 Starting VISTA-MARL greedy agent demo with logging...\n")

    for episode in range(30):
        obs = env.reset()
        done = {agent_id: False for agent_id in obs}
        total_rewards = {agent_id: 0 for agent_id in obs}

        while not all(done.values()):
            actions = {
                agent_id: greedy_action(env.agents[agent_id], env.resources, env.grid_size)
                for agent_id in obs
            }
            obs, rewards, done, _ = env.step(actions)
            for agent_id, reward in rewards.items():
                total_rewards[agent_id] += reward
            env.render()
            print(rewards)
            print("-" * 40)

        total = sum(total_rewards.values())
        writer.writerow([episode + 1, total, total_rewards["agent_0"], total_rewards["agent_1"]])
        print(f"🏁 Episode {episode + 1} finished | Total Reward: {total:.2f}")
        print("=" * 60)
