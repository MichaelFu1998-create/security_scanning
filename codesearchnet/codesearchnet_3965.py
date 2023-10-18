def run(self, data, train_epochs=1000, test_epochs=1000, verbose=None,
            idx=0, lr=0.01, **kwargs):
        """Run the CGNN on a given graph."""
        verbose = SETTINGS.get_default(verbose=verbose)
        optim = th.optim.Adam(self.parameters(), lr=lr)
        self.score.zero_()
        with trange(train_epochs + test_epochs, disable=not verbose) as t:
            for epoch in t:
                optim.zero_grad()
                generated_data = self.forward()
                mmd = self.criterion(generated_data, data)
                if not epoch % 200:
                    t.set_postfix(idx=idx, epoch=epoch, loss=mmd.item())
                mmd.backward()
                optim.step()
                if epoch >= test_epochs:
                    self.score.add_(mmd.data)

        return self.score.cpu().numpy() / test_epochs