def tf_combined_loss(self, states, internals, actions, terminal, reward, next_states, next_internals, update, reference=None):
        """
        Combines Q-loss and demo loss.
        """
        q_model_loss = self.fn_loss(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward,
            next_states=next_states,
            next_internals=next_internals,
            update=update,
            reference=reference
        )

        demo_loss = self.fn_demo_loss(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward,
            update=update,
            reference=reference
        )

        return q_model_loss + self.supervised_weight * demo_loss