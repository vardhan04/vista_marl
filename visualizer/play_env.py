from vista_env.core.env import VISTAEnv

config = {"grid_size": 8, "max_steps": 20, "num_agents": 2, "roles": ["gatherer", "defender"]}
env = VISTAEnv(config)
obs = env.reset()
done = {agent_id: False for agent_id in obs}

while not all(done.values()):
    actions = {agent_id: 0 for agent_id in obs}  # Noop
    obs, rewards, done, _ = env.step(actions)
    env.render()
    print(rewards)
    input("Next step >")