def execute(self, action):
        """
        Pass action to universe environment, return reward, next step, terminal state and
        additional info.

        :param action: action to execute as numpy array, should have dtype np.intc and should adhere to
            the specification given in DeepMindLabEnvironment.action_spec(level_id)
        :return: dict containing the next state, the reward, and a boolean indicating if the
            next state is a terminal state
        """
        adjusted_action = list()
        for action_spec in self.level.action_spec():
            if action_spec['min'] == -1 and action_spec['max'] == 1:
                adjusted_action.append(action[action_spec['name']] - 1)
            else:
                adjusted_action.append(action[action_spec['name']])  # clip?
        action = np.array(adjusted_action, dtype=np.intc)

        reward = self.level.step(action=action, num_steps=self.repeat_action)
        state = self.level.observations()['RGB_INTERLACED']
        terminal = not self.level.is_running()
        return state, terminal, reward