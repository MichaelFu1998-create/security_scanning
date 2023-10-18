def split(self, X, y=None, groups=None):
        """Generate indices to split data into training and test set.
        Parameters
        ----------
        X : array-like, of length n_samples
            Training data, includes reaction's containers
        y : array-like, of length n_samples
            The target variable for supervised learning problems.
        groups : array-like, with shape (n_samples,)
            Group labels for the samples used while splitting the dataset into
            train/test set.
        Yields
        ------
        train : ndarray
            The training set indices for that split.
        test : ndarray
            The testing set indices for that split.
        """
        X, y, groups = indexable(X, y, groups)
        cgrs = [~r for r in X]

        structure_condition = defaultdict(set)

        for structure, condition in zip(cgrs, groups):
            structure_condition[structure].add(condition)

        train_data = defaultdict(list)
        test_data = []

        for n, (structure, condition) in enumerate(zip(cgrs, groups)):
            train_data[condition].append(n)
            if len(structure_condition[structure]) > 1:
                test_data.append(n)

        for condition, indexes in train_data.items():
            test_index = [index for index in indexes if index in test_data]
            if test_index:
                train_index = [i for cond, ind in train_data.items() if cond != condition for i in ind]
                yield array(train_index), array(test_index)