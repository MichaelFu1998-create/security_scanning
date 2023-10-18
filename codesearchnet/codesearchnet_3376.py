def all_events(cls):
        """
        Return all events that all subclasses have so far registered to publish.
        """
        all_evts = set()
        for cls, evts in cls.__all_events__.items():
            all_evts.update(evts)
        return all_evts