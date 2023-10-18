def guess_protocol(self):
        """
        This just generates a string to define the nature of the ABF.
        The ultimate goal is to use info about the abf to guess what to do with it.
            [vc/ic]-[steps/fixed]-[notag/drugs]-[2ch/1ch]
            This represents 2^4 (18) combinations, but is easily expanded.
        """
        clamp="ic"
        if self.units=="pA":
            clamp="vc"
        command="fixed"
        if self.sweeps>1:
            self.setSweep(0)
            P0=str(self.protoX)+str(self.protoY)
            self.setSweep(1)
            P1=str(self.protoX)+str(self.protoY)
            if not P0==P1:
                command="steps"
        tags="notag"
        if len(self.commentSweeps):
            tags="drugs"
        ch="1ch"
        if self.nADC>1:
            ch="2ch"
        guess="-".join([clamp,command,tags,ch])
        return guess