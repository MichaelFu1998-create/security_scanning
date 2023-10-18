def predict_features(self, df_features, df_target, nh=20, idx=0, dropout=0.,
                         activation_function=th.nn.ReLU, lr=0.01, l1=0.1,  batch_size=-1,
                         train_epochs=1000, test_epochs=1000, device=None,
                         verbose=None, nb_runs=3):
        """For one variable, predict its neighbours.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            nh (int): number of hidden units
            idx (int): (optional) for printing purposes
            dropout (float): probability of dropout (between 0 and 1)
            activation_function (torch.nn.Module): activation function of the NN
            lr (float): learning rate of Adam
            l1 (float): L1 penalization coefficient
            batch_size (int): batch size, defaults to full-batch
            train_epochs (int): number of train epochs
            test_epochs (int): number of test epochs
            device (str): cuda or cpu device (defaults to ``cdt.SETTINGS.default_device``)
            verbose (bool): verbosity (defaults to ``cdt.SETTINGS.verbose``)
            nb_runs (int): number of bootstrap runs

        Returns:
            list: scores of each feature relatively to the target

        """
        device, verbose = SETTINGS.get_default(('device', device), ('verbose', verbose))
        x = th.FloatTensor(scale(df_features.values)).to(device)
        y = th.FloatTensor(scale(df_target.values)).to(device)
        out = []
        for i in range(nb_runs):
            model = FSGNN_model([x.size()[1] + 1, nh, 1],
                                dropout=dropout,
                                activation_function=activation_function).to(device)

            out.append(model.train(x, y, lr=0.01, l1=0.1, batch_size=-1,
                                   train_epochs=train_epochs, test_epochs=test_epochs,
                                   device=device, verbose=verbose))
        return list(np.mean(np.array(out), axis=0))