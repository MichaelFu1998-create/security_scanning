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

        condition_structure = defaultdict(set)

        for structure, condition in zip(cgrs, groups):
            condition_structure[condition].add(structure)

        train_data = defaultdict(list)
        test_data = []

        for n, (structure, condition) in enumerate(zip(cgrs, groups)):
            train_data[structure].append(n)
            if len(condition_structure[condition]) > 1:
                test_data.append(n)

        if self.n_splits > len(train_data):
            raise ValueError("Cannot have number of splits n_splits=%d greater"
                             " than the number of transformations: %d."
                             % (self.n_splits, len(train_data)))

        structures_weight = sorted(((x, len(y)) for x, y in train_data.items()), key=lambda x: x[1], reverse=True)
        fold_mean_size = len(cgrs) // self.n_splits

        if structures_weight[0][1] > fold_mean_size:
            warning('You have transformation that greater fold size')

        for idx in range(self.n_repeats):
            train_folds = [[] for _ in range(self.n_splits)]
            for structure, structure_length in structures_weight:
                if self.shuffle:
                    check_random_state(self.random_state).shuffle(train_folds)
                for fold in train_folds[:-1]:
                    if len(fold) + structure_length <= fold_mean_size:
                        fold.extend(train_data[structure])
                        break
                    else:
                        roulette_param = (structure_length - fold_mean_size + len(fold)) / structure_length
                        if random() > roulette_param:
                            fold.extend(train_data[structure])
                            break
                else:
                    train_folds[-1].extend(train_data[structure])

            test_folds = [[] for _ in range(self.n_splits)]
            for test, train in zip(test_folds, train_folds):
                for index in train:
                    if index in test_data:
                        test.append(index)

            for i in range(self.n_splits):
                train_index = []
                for fold in train_folds[:i]:
                    train_index.extend(fold)
                for fold in train_folds[i+1:]:
                    train_index.extend(fold)
                test_index = test_folds[i]
                yield array(train_index), array(test_index)