def _i2p(self, ind, coord):
        """ Translate index info to parameter name """
        return '-'.join([self.param_prefix, str(ind), coord])