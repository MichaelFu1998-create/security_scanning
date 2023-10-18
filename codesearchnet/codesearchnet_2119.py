def as_local_model(self):
        """
        Makes sure our optimizer is wrapped into the global_optimizer meta. This is only relevant for distributed RL.
        """
        super(MemoryModel, self).as_local_model()
        self.optimizer_spec = dict(
            type='global_optimizer',
            optimizer=self.optimizer_spec
        )