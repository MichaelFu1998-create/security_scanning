def get_protocol(self,sweep):
        """
        given a sweep, return the protocol as [Xs,Ys].
        This is good for plotting/recreating the protocol trace.
        There may be duplicate numbers.
        """
        self.setsweep(sweep)
        return list(self.protoX),list(self.protoY)