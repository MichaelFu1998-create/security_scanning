def objs(self):
        """
        Returns a generator list of tracked objects which are recognized with
        this profile and are in the current session.
        """
        for obj in self.objects.itervalues():
            if obj.sessionid in self.sessions:
                yield obj