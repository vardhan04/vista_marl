# import numpy as np
# import random

# class VISTAEnv:
#     def __init__(self, config):
#         self.grid_size = config.get("grid_size", 10)
#         self.max_steps = config.get("max_steps", 100)
#         self.num_agents = config.get("num_agents", 2)
#         self.agent_roles = config.get("roles", ["gatherer", "defender"])
#         self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
#         self.agents = {}
#         self.resources = set()
#         self.obstacles = set()
#         self.step_count = 0
#         self.reset()

#     def reset(self):
#         self.grid.fill(0)
#         self.agents = {}
#         self.resources = set()
#         self.obstacles = set()
#         self.step_count = 0

#         for i in range(self.num_agents):
#             while True:
#                 r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
#                 if self.grid[r, c] == 0:
#                     self.agents[f"agent_{i}"] = (r, c)
#                     self.grid[r, c] = 2
#                     break

#         for _ in range(5):
#             r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
#             if self.grid[r, c] == 0:
#                 self.resources.add((r, c))
#                 self.grid[r, c] = 3

#         for _ in range(8):
#             r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
#             if self.grid[r, c] == 0:
#                 self.obstacles.add((r, c))
#                 self.grid[r, c] = 1

#         obs = {agent: self._observe(agent) for agent in self.agents}
#         return obs

#     def _observe(self, agent_id):
#         return np.copy(self.grid)

#     def step(self, actions):
#         rewards = {}
#         done = {}
#         info = {}
#         self.step_count += 1

#         for agent_id, action in actions.items():
#             r, c = self.agents[agent_id]
#             dr, dc = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)][action]
#             nr, nc = r + dr, c + dc

#             if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr, nc] != 1:
#                 self.grid[r, c] = 0
#                 if (nr, nc) in self.resources:
#                     rewards[agent_id] = 10
#                     self.resources.remove((nr, nc))
#                 else:
#                     rewards[agent_id] = -0.1
#                 self.agents[agent_id] = (nr, nc)
#                 self.grid[nr, nc] = 2
#             else:
#                 rewards[agent_id] = -0.5

#             done[agent_id] = False

#         if self.step_count >= self.max_steps or not self.resources:
#             done = {agent: True for agent in self.agents}

#         obs = {agent: self._observe(agent) for agent in self.agents}
#         return obs, rewards, done, info

#     def render(self):
#         visual = []
#         for r in range(self.grid_size):
#             row = ""
#             for c in range(self.grid_size):
#                 if (r, c) in self.agents.values():
#                     agent_id = [k for k, v in self.agents.items() if v == (r, c)][0]
#                     row += f"🧍{agent_id[-1]}"
#                 elif (r, c) in self.resources:
#                     row += "💎 "
#                 elif (r, c) in self.obstacles:
#                     row += "🧱 "
#                 else:
#                     row += "⬜ "
#             visual.append(row)
#         print("\n".join(visual))


import numpy as np
import random

class VISTAEnv:
    def __init__(self, config):
        self.grid_size = config.get("grid_size", 10)
        self.max_steps = config.get("max_steps", 100)
        self.num_agents = config.get("num_agents", 2)
        self.agent_roles = config.get("roles", ["hacker"] * self.num_agents)
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.agents = {}
        self.directions = {}
        self.alive = {}
        self.resources = set()
        self.obstacles = set()
        self.step_count = 0
        self.reset()

    def reset(self):
        self.grid.fill(0)
        self.agents = {}
        self.resources = set()
        self.obstacles = set()
        self.directions = {}
        self.alive = {}
        self.step_count = 0

        for i in range(self.num_agents):
            while True:
                r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if self.grid[r, c] == 0:
                    agent_id = f"agent_{i}"
                    self.agents[agent_id] = (r, c)
                    self.directions[agent_id] = random.choice(['N', 'S', 'E', 'W'])
                    self.alive[agent_id] = True
                    self.grid[r, c] = 2
                    break

        for _ in range(5):
            r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if self.grid[r, c] == 0:
                self.resources.add((r, c))
                self.grid[r, c] = 3

        for _ in range(8):
            r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if self.grid[r, c] == 0:
                self.obstacles.add((r, c))
                self.grid[r, c] = 1

        obs = {agent: self._observe(agent) for agent in self.agents}
        return obs

    def _observe(self, agent_id):
        if not self.alive[agent_id]:
            return np.full((self.grid_size, self.grid_size), -1)
        return np.copy(self.grid)

    def step(self, actions):
        rewards = {agent: 0 for agent in self.agents}
        done = {}
        info = {}
        self.step_count += 1

        proposed_pos = {}
        for agent_id, action in actions.items():
            if not self.alive[agent_id]:
                continue
            r, c = self.agents[agent_id]
            dr, dc, facing = [(0, 0, self.directions[agent_id]), 
                              (-1, 0, 'N'), (1, 0, 'S'),
                              (0, -1, 'W'), (0, 1, 'E')][action]
            nr, nc = r + dr, c + dc
            self.directions[agent_id] = facing

            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr, nc] != 1:
                proposed_pos[agent_id] = (nr, nc)
            else:
                rewards[agent_id] -= 1  # hit wall or invalid
                proposed_pos[agent_id] = (r, c)  # stays

        # Handle backstabs first
        for attacker, pos in proposed_pos.items():
            for victim, (vr, vc) in self.agents.items():
                if attacker == victim or not self.alive[victim] or not self.alive[attacker]:
                    continue
                if pos == (vr, vc):  # same cell check happens later
                    continue
                if self._is_behind(attacker, victim):
                    self.alive[victim] = False
                    rewards[attacker] += 50
                    rewards[victim] -= 100

        # Handle conflicts (multiple agents to same cell)
        cell_to_agents = {}
        for agent_id, pos in proposed_pos.items():
            if not self.alive[agent_id]:
                continue
            cell_to_agents.setdefault(pos, []).append(agent_id)

        for pos, contenders in cell_to_agents.items():
            if len(contenders) > 1:
                survivor = random.choice(contenders)
                for agent_id in contenders:
                    if agent_id == survivor:
                        rewards[agent_id] += 20
                    else:
                        self.alive[agent_id] = False
                        rewards[agent_id] -= 100
            else:
                agent_id = contenders[0]
                old_r, old_c = self.agents[agent_id]
                new_r, new_c = pos
                self.grid[old_r, old_c] = 0
                self.agents[agent_id] = pos
                if pos in self.resources:
                    rewards[agent_id] += 10
                    self.resources.remove(pos)
                else:
                    rewards[agent_id] += 0.1 * self.step_count
                self.grid[new_r, new_c] = 2

        # Determine done
        all_dead = all(not self.alive[agent] for agent in self.agents)
        if all_dead or self.step_count >= self.max_steps or not self.resources:
            done = {agent: True for agent in self.agents}
        else:
            done = {agent: not self.alive[agent] for agent in self.agents}

        obs = {agent: self._observe(agent) for agent in self.agents}
        print("🧠 STEP DEBUG LOG")
        for agent in self.agents:
            print(f"  🔹 {agent}: Alive={self.alive[agent]}, Pos={self.agents[agent]}, Dir={self.directions[agent]}")

        print("\n🔍 DEATH EVENTS")
        for attacker, pos in proposed_pos.items():
            for victim, victim_pos in self.agents.items():
                if attacker == victim or not self.alive[victim] or not self.alive[attacker]:
                    continue
                if self._is_behind(attacker, victim):
                    print(f"  🗡️ {attacker} backstabbed {victim} at {victim_pos}")

        # For conflict resolution
        for pos, contenders in cell_to_agents.items():
            if len(contenders) > 1:
                print(f"  ⚔️ Conflict at {pos}: {contenders} → One survived")

        print("\n🎯 REWARDS")
        for agent_id, reward in rewards.items():
            print(f"  💰 {agent_id}: {reward}")
        print("-" * 60)
        return obs, rewards, done, info

    def _is_behind(self, attacker, victim):
        if not self.alive[attacker] or not self.alive[victim]:
            return False
        ar, ac = self.agents[attacker]
        vr, vc = self.agents[victim]
        facing = self.directions[victim]
        if facing == 'N' and (ar, ac) == (vr + 1, vc):
            return True
        if facing == 'S' and (ar, ac) == (vr - 1, vc):
            return True
        if facing == 'E' and (ar, ac) == (vr, vc - 1):
            return True
        if facing == 'W' and (ar, ac) == (vr, vc + 1):
            return True
        return False

    def render(self):
        visual = []
        for r in range(self.grid_size):
            row = ""
            for c in range(self.grid_size):
                agent_here = [k for k, v in self.agents.items() if v == (r, c) and self.alive[k]]
                if agent_here:
                    agent_id = agent_here[0]
                    row += f"🧍{agent_id[-1]}"
                elif (r, c) in self.resources:
                    row += "💎 "
                elif (r, c) in self.obstacles:
                    row += "🧱 "
                else:
                    row += "⬜ "
            visual.append(row)
        print("\n".join(visual))
