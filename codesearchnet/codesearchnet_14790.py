def get_public_net_id(self):
        """Returns the public net id"""
        for id, net_params in self.strategy.iteritems():
            if id == CONF.QUARK.public_net_id:
                return id
        return None