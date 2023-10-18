def fit(self, X, y=None):
        """
        Build a trainer and run main_loop.

        Parameters
        ----------
        X : array_like
            Training examples.
        y : array_like, optional
            Labels.
        """
        from pylearn2.config import yaml_parse
        from pylearn2.train import Train

        # build trainer
        params = self.get_params()
        yaml_string = Template(self.yaml_string).substitute(params)
        self.trainer = yaml_parse.load(yaml_string)
        assert isinstance(self.trainer, Train)
        if self.trainer.dataset is not None:
            raise ValueError('Train YAML database must evaluate to None.')
        self.trainer.dataset = self._get_dataset(X, y)

        # update monitoring dataset(s)
        if (hasattr(self.trainer.algorithm, 'monitoring_dataset') and
                self.trainer.algorithm.monitoring_dataset is not None):
            monitoring_dataset = self.trainer.algorithm.monitoring_dataset
            if len(monitoring_dataset) == 1 and '' in monitoring_dataset:
                monitoring_dataset[''] = self.trainer.dataset
            else:
                monitoring_dataset['train'] = self.trainer.dataset
            self.trainer.algorithm._set_monitoring_dataset(monitoring_dataset)
        else:
            self.trainer.algorithm._set_monitoring_dataset(
                self.trainer.dataset)

        # run main loop
        self.trainer.main_loop()