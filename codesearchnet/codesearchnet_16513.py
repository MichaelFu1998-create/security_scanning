def initialize(self):
        """Initialize the corresponding DXclass from the data.

        class = DXInitObject.initialize()
        """
        return self.DXclasses[self.type](self.id,**self.args)