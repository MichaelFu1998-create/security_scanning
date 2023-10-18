def clone_worker_agent(agent, factor, environment, network, agent_config):
    """
    Clones a given Agent (`factor` times) and returns a list of the cloned Agents with the original Agent
    in the first slot.

    Args:
        agent (Agent): The Agent object to clone.
        factor (int): The length of the final list.
        environment (Environment): The Environment to use for all cloned agents.
        network (LayeredNetwork): The Network to use (or None) for an Agent's Model.
        agent_config (dict): A dict of Agent specifications passed into the Agent's c'tor as kwargs.
    Returns:
        The list with `factor` cloned agents (including the original one).
    """
    ret = [agent]
    for i in xrange(factor - 1):
        worker = WorkerAgentGenerator(type(agent))(
            states=environment.states,
            actions=environment.actions,
            network=network,
            model=agent.model,
            **agent_config
        )
        ret.append(worker)

    return ret