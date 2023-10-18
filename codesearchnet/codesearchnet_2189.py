def import_demonstrations(self, demonstrations):
        """
        Imports demonstrations, i.e. expert observations. Note that for large numbers of observations,
        set_demonstrations is more appropriate, which directly sets memory contents to an array an expects
        a different layout.

        Args:
            demonstrations: List of observation dicts
        """
        if isinstance(demonstrations, dict):
            if self.unique_state:
                demonstrations['states'] = dict(state=demonstrations['states'])
            if self.unique_action:
                demonstrations['actions'] = dict(action=demonstrations['actions'])

            self.model.import_demo_experience(**demonstrations)

        else:
            if self.unique_state:
                states = dict(state=list())
            else:
                states = {name: list() for name in demonstrations[0]['states']}
            internals = {name: list() for name in demonstrations[0]['internals']}
            if self.unique_action:
                actions = dict(action=list())
            else:
                actions = {name: list() for name in demonstrations[0]['actions']}
            terminal = list()
            reward = list()

            for demonstration in demonstrations:
                if self.unique_state:
                    states['state'].append(demonstration['states'])
                else:
                    for name, state in states.items():
                        state.append(demonstration['states'][name])
                for name, internal in internals.items():
                    internal.append(demonstration['internals'][name])
                if self.unique_action:
                    actions['action'].append(demonstration['actions'])
                else:
                    for name, action in actions.items():
                        action.append(demonstration['actions'][name])
                terminal.append(demonstration['terminal'])
                reward.append(demonstration['reward'])

            self.model.import_demo_experience(
                states=states,
                internals=internals,
                actions=actions,
                terminal=terminal,
                reward=reward
            )