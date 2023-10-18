def inheritFromContext(self, ignore=()):
        """
        Doesn't store exactly the same items as Nodebox for ease of implementation,
        it has enough to get the Nodebox Dentrite example working.
        """
        for canvas_attr, grob_attr in STATES.items():
            if canvas_attr in ignore:
                continue
            setattr(self, grob_attr, getattr(self._bot._canvas, canvas_attr))