def refresh(self):
        """reset output buffer, re-parse entire source file, and return output
        
        Since parsing involves a good deal of randomness, this is an
        easy way to get new output without having to reload a grammar file
        each time.
        """
        self.reset()
        self.parse(self.source)
        return self.output()