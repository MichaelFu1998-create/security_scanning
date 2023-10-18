def get_protocol_sequence(self,sweep):
        """
        given a sweep, return the protocol as condensed sequence.
        This is better for comparing similarities and determining steps.
        There should be no duplicate numbers.
        """
        self.setsweep(sweep)
        return list(self.protoSeqX),list(self.protoSeqY)