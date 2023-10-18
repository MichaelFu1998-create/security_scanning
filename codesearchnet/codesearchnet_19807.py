def setsweeps(self):
        """iterate over every sweep"""
        for sweep in range(self.sweeps):
            self.setsweep(sweep)
            yield self.sweep