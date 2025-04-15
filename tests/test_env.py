
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from vista_env.core.env import VISTAEnv

def test_env_runs():
    config = {"grid_size": 5, "max_steps": 10, "num_agents": 1, "roles": ["gatherer"]}
    env = VISTAEnv(config)
    obs = env.reset()
    for _ in range(5):
        actions = {k: 0 for k in obs}
        obs, rewards, done, info = env.step(actions)
    assert isinstance(obs, dict)
    assert all(isinstance(r, (int, float)) for r in rewards.values())