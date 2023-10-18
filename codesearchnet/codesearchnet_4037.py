def run(self, x, y, lr=0.01, train_epochs=1000, test_epochs=1000, idx=0, verbose=None, **kwargs):
        """Run the GNN on a pair x,y of FloatTensor data."""
        verbose = SETTINGS.get_default(verbose=verbose)
        optim = th.optim.Adam(self.parameters(), lr=lr)
        running_loss = 0
        teloss = 0

        for i in range(train_epochs + test_epochs):
            optim.zero_grad()
            pred = self.forward(x)
            loss = self.criterion(pred, y)
            running_loss += loss.item()

            if i < train_epochs:
                loss.backward()
                optim.step()
            else:
                teloss += running_loss

            # print statistics
            if verbose and not i % 300:
                print('Idx:{}; epoch:{}; score:{}'.
                      format(idx, i, running_loss/300))
                running_loss = 0.0

        return teloss / test_epochs