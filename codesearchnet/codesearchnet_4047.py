def forward(self, x):
        """Passing data through the network.

        :param x: 2d tensor containing both (x,y) Variables
        :return: output of the net
        """

        features = self.conv(x).mean(dim=2)
        return self.dense(features)