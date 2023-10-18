def fit(self, trX, trY, batch_size=64, n_epochs=1, len_filter=LenFilter(), snapshot_freq=1, path=None):
        """Train model on given training examples and return the list of costs after each minibatch is processed.

        Args:
          trX (list) -- Inputs
          trY (list) -- Outputs
          batch_size (int, optional) -- number of examples in a minibatch (default 64)
          n_epochs (int, optional)  -- number of epochs to train for (default 1)
          len_filter (object, optional) -- object to filter training example by length (default LenFilter())
          snapshot_freq (int, optional) -- number of epochs between saving model snapshots (default 1)
          path (str, optional) -- prefix of path where model snapshots are saved.
            If None, no snapshots are saved (default None)

        Returns:
          list -- costs of model after processing each minibatch
        """
        if len_filter is not None:
            trX, trY = len_filter.filter(trX, trY)
        trY = standardize_targets(trY, cost=self.cost)

        n = 0.
        t = time()
        costs = []
        for e in range(n_epochs):
            epoch_costs = []
            for xmb, ymb in self.iterator.iterXY(trX, trY):
                c = self._train(xmb, ymb)
                epoch_costs.append(c)
                n += len(ymb)
                if self.verbose >= 2:
                    n_per_sec = n / (time() - t)
                    n_left = len(trY) - n % len(trY)
                    time_left = n_left/n_per_sec
                    sys.stdout.write("\rEpoch %d Seen %d samples Avg cost %0.4f Time left %d seconds" % (e, n, np.mean(epoch_costs[-250:]), time_left))
                    sys.stdout.flush()
            costs.extend(epoch_costs)

            status = "Epoch %d Seen %d samples Avg cost %0.4f Time elapsed %d seconds" % (e, n, np.mean(epoch_costs[-250:]), time() - t)
            if self.verbose >= 2:
                sys.stdout.write("\r"+status)
                sys.stdout.flush()
                sys.stdout.write("\n")
            elif self.verbose == 1:
                print(status)
            if path and e % snapshot_freq == 0:
                save(self, "{0}.{1}".format(path, e))
        return costs