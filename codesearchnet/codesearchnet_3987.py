def forward(self, x):
        """Feed-forward the model."""
        return self.layers(x * (self._filter *
                                self.fs_filter).expand_as(x))