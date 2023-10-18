def forward(self, x):
        """Pass data through the net structure.

        :param x: input data: shape (:,1)
        :type x: torch.Variable
        :return: output of the shallow net
        :rtype: torch.Variable

        """
        self.noise.normal_()
        return self.layers(th.cat([x, self.noise], 1))