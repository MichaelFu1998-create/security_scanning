def in_use(self):
        """Returns True if there is a :class:`State` object that uses this
        ``Flow``"""
        state = State.objects.filter(flow=self).first()
        return bool(state)