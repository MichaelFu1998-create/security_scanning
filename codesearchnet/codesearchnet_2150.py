def import_experience(self, experiences):
        """
        Imports experiences.

        Args:
            experiences: 
        """
        if isinstance(experiences, dict):
            if self.unique_state:
                experiences['states'] = dict(state=experiences['states'])
            if self.unique_action:
                experiences['actions'] = dict(action=experiences['actions'])

            self.model.import_experience(**experiences)

        else:
            if self.unique_state:
                states = dict(state=list())
            else:
                states = {name: list() for name in experiences[0]['states']}
            internals = [list() for _ in experiences[0]['internals']]
            if self.unique_action:
                actions = dict(action=list())
            else:
                actions = {name: list() for name in experiences[0]['actions']}
            terminal = list()
            reward = list()

            for experience in experiences:
                if self.unique_state:
                    states['state'].append(experience['states'])
                else:
                    for name in sorted(states):
                        states[name].append(experience['states'][name])
                for n, internal in enumerate(internals):
                    internal.append(experience['internals'][n])
                if self.unique_action:
                    actions['action'].append(experience['actions'])
                else:
                    for name in sorted(actions):
                        actions[name].append(experience['actions'][name])
                terminal.append(experience['terminal'])
                reward.append(experience['reward'])

            self.model.import_experience(
                states=states,
                internals=internals,
                actions=actions,
                terminal=terminal,
                reward=reward
            )