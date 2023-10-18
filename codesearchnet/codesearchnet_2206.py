def create_distributions(self):
        """
        Creates and returns the Distribution objects based on self.distributions_spec.

        Returns: Dict of distributions according to self.distributions_spec.
        """
        distributions = dict()
        for name in sorted(self.actions_spec):
            action = self.actions_spec[name]

            if self.distributions_spec is not None and name in self.distributions_spec:
                kwargs = dict(action)
                kwargs['scope'] = name
                kwargs['summary_labels'] = self.summary_labels
                distributions[name] = Distribution.from_spec(
                    spec=self.distributions_spec[name],
                    kwargs=kwargs
                )

            elif action['type'] == 'bool':
                distributions[name] = Bernoulli(
                    shape=action['shape'],
                    scope=name,
                    summary_labels=self.summary_labels
                )

            elif action['type'] == 'int':
                distributions[name] = Categorical(
                    shape=action['shape'],
                    num_actions=action['num_actions'],
                    scope=name,
                    summary_labels=self.summary_labels
                )

            elif action['type'] == 'float':
                if 'min_value' in action:
                    distributions[name] = Beta(
                        shape=action['shape'],
                        min_value=action['min_value'],
                        max_value=action['max_value'],
                        scope=name,
                        summary_labels=self.summary_labels
                    )

                else:
                    distributions[name] = Gaussian(
                        shape=action['shape'],
                        scope=name,
                        summary_labels=self.summary_labels
                    )

        return distributions