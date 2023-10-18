def WorkerAgentGenerator(agent_class):
    """
    Worker Agent generator, receives an Agent class and creates a Worker Agent class that inherits from that Agent.
    """

    # Support special case where class is given as type-string (AgentsDictionary) or class-name-string.
    if isinstance(agent_class, str):
        agent_class = AgentsDictionary.get(agent_class)
        # Last resort: Class name given as string?
        if not agent_class and agent_class.find('.') != -1:
            module_name, function_name = agent_class.rsplit('.', 1)
            module = importlib.import_module(module_name)
            agent_class = getattr(module, function_name)

    class WorkerAgent(agent_class):
        """
        Worker agent receiving a shared model to avoid creating multiple models.
        """

        def __init__(self, model=None, **kwargs):
            # Set our model externally.
            self.model = model
            # Be robust against `network` coming in from kwargs even though this agent doesn't have one
            if not issubclass(agent_class, LearningAgent):
                kwargs.pop("network")
            # Call super c'tor (which will call initialize_model and assign self.model to the return value).
            super(WorkerAgent, self).__init__(**kwargs)

        def initialize_model(self):
            # Return our model (already given and initialized).
            return self.model

    return WorkerAgent