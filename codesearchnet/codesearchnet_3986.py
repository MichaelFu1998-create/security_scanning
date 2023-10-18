def forward(self, input):
        """Feed-forward through the network."""
        return th.nn.functional.linear(input, self.weight.div(self.weight.pow(2).sum(0).sqrt()))