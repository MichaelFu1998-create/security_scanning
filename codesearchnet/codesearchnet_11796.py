def unregister(self):
        """
        Removes this satchel from global registeries.
        """

        for k in list(env.keys()):
            if k.startswith(self.env_prefix):
                del env[k]

        try:
            del all_satchels[self.name.upper()]
        except KeyError:
            pass

        try:
            del manifest_recorder[self.name]
        except KeyError:
            pass

        try:
            del manifest_deployers[self.name.upper()]
        except KeyError:
            pass

        try:
            del manifest_deployers_befores[self.name.upper()]
        except KeyError:
            pass

        try:
            del required_system_packages[self.name.upper()]
        except KeyError:
            pass