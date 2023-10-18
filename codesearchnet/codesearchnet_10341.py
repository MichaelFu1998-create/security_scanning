def register(self,flag):
        """Register a new :class:`Flag` instance with the Flags registry."""
        super(Flags,self).__setitem__(flag.name,flag)