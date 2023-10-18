def gather_configs(self):
        """
        Gather configuration requirements of all plugins
        """
        configs = []
        for what in self.order:
            for key in self.plugins[what]:
                mgr = self.plugins[what][key]
                c = mgr.config(what='get')
                if c is not None:
                    c.update({
                        'description': mgr.description
                    })
                    # print("Gathering configuration from ", c)
                    configs.append(c)
        return configs