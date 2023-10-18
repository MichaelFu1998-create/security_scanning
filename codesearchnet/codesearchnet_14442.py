def load(self):
        """
        Load the dataset using pylearn2.config.yaml_parse.
        """
        from pylearn2.config import yaml_parse
        from pylearn2.datasets import Dataset

        dataset = yaml_parse.load(self.yaml_string)
        assert isinstance(dataset, Dataset)
        data = dataset.iterator(mode='sequential', num_batches=1,
                                data_specs=dataset.data_specs,
                                return_tuple=True).next()
        if len(data) == 2:
            X, y = data
            y = np.squeeze(y)
            if self.one_hot:
                y = np.argmax(y, axis=1)
        else:
            X = data
            y = None
        return X, y