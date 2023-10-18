def cleanup_none(self):
        """
        Removes the temporary value set for None attributes.
        """
        for (prop, default) in self.defaults.items():
            if getattr(self, prop) == '_None':
                setattr(self, prop, None)