def fit(self, x_tr, y_tr, epochs=50, batchsize=32,
            learning_rate=0.01, verbose=None, device=None):
        """Fit the NCC model.

        Args:
            x_tr (pd.DataFrame): CEPC format dataframe containing the pairs
            y_tr (pd.DataFrame or np.ndarray): labels associated to the pairs
            epochs (int): number of train epochs
            learning_rate (float): learning rate of Adam
            verbose (bool): verbosity (defaults to ``cdt.SETTINGS.verbose``)
            device (str): cuda or cpu device (defaults to ``cdt.SETTINGS.default_device``)
        """
        if batchsize > len(x_tr):
            batchsize = len(x_tr)
        verbose, device = SETTINGS.get_default(('verbose', verbose),
                                               ('device', device))
        self.model = NCC_model()
        opt = th.optim.Adam(self.model.parameters(), lr=learning_rate)
        criterion = th.nn.BCEWithLogitsLoss()
        y = y_tr.values if isinstance(y_tr, pd.DataFrame) else y_tr
        y = th.Tensor(y)/2 + .5
        # print(y)
        self.model = self.model.to(device)
        y = y.to(device)
        dataset = []
        for i, (idx, row) in enumerate(x_tr.iterrows()):

            a = row['A'].reshape((len(row['A']), 1))
            b = row['B'].reshape((len(row['B']), 1))
            m = np.hstack((a, b))
            m = m.astype('float32')
            m = th.from_numpy(m).t().unsqueeze(0)
            dataset.append(m)
        dataset = [m.to(device) for m in dataset]
        acc = [0]
        da = th.utils.data.DataLoader(Dataset(dataset, y), batch_size=batchsize,
                                      shuffle=True)
        data_per_epoch = (len(dataset) // batchsize)
        with trange(epochs, desc="Epochs", disable=not verbose) as te:
            for epoch in te:
                with trange(data_per_epoch, desc="Batches of {}".format(batchsize),
                            disable=not (verbose and batchsize == len(dataset))) as t:
                    output = []
                    labels = []
                    for (batch, label), i in zip(da, t):
                        opt.zero_grad()
                        # print(batch.shape, labels.shape)
                        out = th.stack([self.model(m) for m in batch], 0).squeeze(2)
                        loss = criterion(out, label)
                        loss.backward()
                        t.set_postfix(loss=loss.item())
                        opt.step()
                        output.append(out)
                        labels.append(label)
                    acc = th.where(th.cat(output, 0) > .5,
                                   th.ones(len(output)),
                                   th.zeros(len(output))) - th.cat(labels, 0)
                    te.set_postfix(Acc=1-acc.abs().mean().item())