def forward_events_to(self, sink, include_source=False):
        """This forwards signal to sink"""
        assert isinstance(sink, Eventful), f'{sink.__class__.__name__} is not Eventful'
        self._forwards[sink] = include_source