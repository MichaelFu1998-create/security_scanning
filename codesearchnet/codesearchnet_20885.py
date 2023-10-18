def follow_markers(self, start=0, end=1e100, states=None):
        '''Iterate over a set of marker data, dragging its skeleton along.

        Parameters
        ----------
        start : int, optional
            Start following marker data after this frame. Defaults to 0.
        end : int, optional
            Stop following marker data after this frame. Defaults to the end of
            the marker data.
        states : list of body states, optional
            If given, set the states of the skeleton bodies to these values
            before starting to follow the marker data.
        '''
        if states is not None:
            self.skeleton.set_body_states(states)
        for frame_no, frame in enumerate(self.markers):
            if frame_no < start:
                continue
            if frame_no >= end:
                break
            for states in self._step_to_marker_frame(frame_no):
                yield states