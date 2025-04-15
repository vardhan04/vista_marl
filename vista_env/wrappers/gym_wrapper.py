from gymnasium import Env
from vista_env.core.env import VISTAEnv

class VISTAGymWrapper(Env):
    def __init__(self, config):
        self.env = VISTAEnv(config)
        self.action_space = None
        self.observation_space = None

    def reset(self):
        return self.env.reset()

    def step(self, actions):
        return self.env.step(actions)

    def render(self):
        self.env.render()