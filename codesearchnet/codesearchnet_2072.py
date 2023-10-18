def execute(self, action):
        """
        Executes a single step in the UE4 game. This step may be comprised of one or more actual game ticks for all of
        which the same given
        action- and axis-inputs (or action number in case of discretized actions) are repeated.
        UE4 distinguishes between action-mappings, which are boolean actions (e.g. jump or dont-jump) and axis-mappings,
        which are continuous actions
        like MoveForward with values between -1.0 (run backwards) and 1.0 (run forwards), 0.0 would mean: stop.
        """
        action_mappings, axis_mappings = [], []

        # TODO: what if more than one actions are passed?

        # Discretized -> each action is an int
        if self.discretize_actions:
            # Pull record from discretized_actions, which will look like: [A, Right, SpaceBar].
            combination = self.discretized_actions[action]
            # Translate to {"axis_mappings": [('A', 1.0), (Right, 1.0)], "action_mappings": [(SpaceBar, True)]}
            for key, value in combination:
                # Action mapping (True or False).
                if isinstance(value, bool):
                    action_mappings.append((key, value))
                # Axis mapping: always use 1.0 as value as UE4 already multiplies with the correct scaling factor.
                else:
                    axis_mappings.append((key, value))
        # Non-discretized: Each action is a dict of action- and axis-mappings defined in UE4 game's input settings.
        # Re-translate Incoming action names into keyboard keys for the server.
        elif action:
            try:
                action_mappings, axis_mappings = self.translate_abstract_actions_to_keys(action)
            except KeyError as e:
                raise TensorForceError("Action- or axis-mapping with name '{}' not defined in connected UE4 game!".
                                       format(e))

        # message = {"cmd": "step", 'delta_time': 0.33,
        #     'actions': [('X', True), ('Y', False)],
        #     'axes': [('Left': 1.0), ('Up': -1.0)]
        # }
        message = dict(
            cmd="step",
            delta_time=self.delta_time,
            num_ticks=self.num_ticks,
            actions=action_mappings,
            axes=axis_mappings
        )
        self.protocol.send(message, self.socket)
        # Wait for response (blocks).
        response = self.protocol.recv(self.socket)
        r = response.pop(b"_reward", 0.0)
        is_terminal = response.pop(b"_is_terminal", False)

        obs = self.extract_observation(response)
        # Cache last observation
        self.last_observation = obs
        return obs, is_terminal, r