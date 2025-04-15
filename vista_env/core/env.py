import numpy as np
import random

class VISTAEnv:
    def __init__(self, config):
        self.grid_size = config.get("grid_size", 10)
        self.max_steps = config.get("max_steps", 100)
        self.num_agents = config.get("num_agents", 2)
        self.agent_roles = config.get("roles", ["gatherer", "defender"])
        self.grid = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.agents = {}
        self.resources = set()
        self.obstacles = set()
        self.step_count = 0
        self.reset()

    def reset(self):
        self.grid.fill(0)
        self.agents = {}
        self.resources = set()
        self.obstacles = set()
        self.step_count = 0

        for i in range(self.num_agents):
            while True:
                r, c = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if self.grid[r, c] == 0:
                    self.agents[f"agent_{i}"] = (r, c)
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
        return np.copy(self.grid)

    def step(self, actions):
        rewards = {}
        done = {}
        info = {}
        self.step_count += 1

        for agent_id, action in actions.items():
            r, c = self.agents[agent_id]
            dr, dc = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)][action]
            nr, nc = r + dr, c + dc

            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size and self.grid[nr, nc] != 1:
                self.grid[r, c] = 0
                if (nr, nc) in self.resources:
                    rewards[agent_id] = 10
                    self.resources.remove((nr, nc))
                else:
                    rewards[agent_id] = -0.1
                self.agents[agent_id] = (nr, nc)
                self.grid[nr, nc] = 2
            else:
                rewards[agent_id] = -0.5

            done[agent_id] = False

        if self.step_count >= self.max_steps or not self.resources:
            done = {agent: True for agent in self.agents}

        obs = {agent: self._observe(agent) for agent in self.agents}
        return obs, rewards, done, info

    def render(self):
        visual = []
        for r in range(self.grid_size):
            row = ""
            for c in range(self.grid_size):
                if (r, c) in self.agents.values():
                    agent_id = [k for k, v in self.agents.items() if v == (r, c)][0]
                    row += f"🧍{agent_id[-1]}"
                elif (r, c) in self.resources:
                    row += "💎 "
                elif (r, c) in self.obstacles:
                    row += "🧱 "
                else:
                    row += "⬜ "
            visual.append(row)
        print("\n".join(visual))
