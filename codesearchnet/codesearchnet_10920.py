def compact_name(self, hashsize=6):
        """Compact representation of all simulation parameters
        """
        # this can be made more robust for ID > 9 (double digit)
        s = self.compact_name_core(hashsize, t_max=True)
        s += "_ID%d-%d" % (self.ID, self.EID)
        return s