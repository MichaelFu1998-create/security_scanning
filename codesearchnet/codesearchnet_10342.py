def update(self,*flags):
        """Update Flags registry with a list of :class:`Flag` instances."""
        super(Flags,self).update([(flag.name,flag) for flag in flags])