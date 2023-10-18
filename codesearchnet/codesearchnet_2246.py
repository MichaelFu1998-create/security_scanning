def tf_demo_loss(self, states, actions, terminal, reward, internals, update, reference=None):
        """
        Extends the q-model loss via the dqfd large-margin loss.
        """
        embedding = self.network.apply(x=states, internals=internals, update=update)
        deltas = list()

        for name in sorted(actions):
            action = actions[name]
            distr_params = self.distributions[name].parameterize(x=embedding)
            state_action_value = self.distributions[name].state_action_value(distr_params=distr_params, action=action)

            # Create the supervised margin loss
            # Zero for the action taken, one for all other actions, now multiply by expert margin
            if self.actions_spec[name]['type'] == 'bool':
                num_actions = 2
                action = tf.cast(x=action, dtype=util.tf_dtype('int'))
            else:
                num_actions = self.actions_spec[name]['num_actions']

            one_hot = tf.one_hot(indices=action, depth=num_actions)
            ones = tf.ones_like(tensor=one_hot, dtype=tf.float32)
            inverted_one_hot = ones - one_hot

            # max_a([Q(s,a) + l(s,a_E,a)], l(s,a_E, a) is 0 for expert action and margin value for others
            state_action_values = self.distributions[name].state_action_value(distr_params=distr_params)
            state_action_values = state_action_values + inverted_one_hot * self.expert_margin
            supervised_selector = tf.reduce_max(input_tensor=state_action_values, axis=-1)

            # J_E(Q) = max_a([Q(s,a) + l(s,a_E,a)] - Q(s,a_E)
            delta = supervised_selector - state_action_value

            action_size = util.prod(self.actions_spec[name]['shape'])
            delta = tf.reshape(tensor=delta, shape=(-1, action_size))
            deltas.append(delta)

        loss_per_instance = tf.reduce_mean(input_tensor=tf.concat(values=deltas, axis=1), axis=1)
        loss_per_instance = tf.square(x=loss_per_instance)

        return tf.reduce_mean(input_tensor=loss_per_instance, axis=0)