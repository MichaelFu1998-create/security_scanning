def settle_to_markers(self, frame_no=0, max_distance=0.05, max_iters=300,
                          states=None):
        '''Settle the skeleton to our marker data at a specific frame.

        Parameters
        ----------
        frame_no : int, optional
            Settle the skeleton to marker data at this frame. Defaults to 0.
        max_distance : float, optional
            The settling process will stop when the mean marker distance falls
            below this threshold. Defaults to 0.1m (10cm). Setting this too
            small prevents the settling process from finishing (it will loop
            indefinitely), and setting it too large prevents the skeleton from
            settling to a stable state near the markers.
        max_iters : int, optional
            Attempt to settle markers for at most this many iterations. Defaults
            to 1000.
        states : list of body states, optional
            If given, set the bodies in our skeleton to these kinematic states
            before starting the settling process.
        '''
        if states is not None:
            self.skeleton.set_body_states(states)
        dist = None
        for _ in range(max_iters):
            for _ in self._step_to_marker_frame(frame_no):
                pass
            dist = np.nanmean(abs(self.markers.distances()))
            logging.info('settling to frame %d: marker distance %.3f', frame_no, dist)
            if dist < max_distance:
                return self.skeleton.get_body_states()
            for b in self.skeleton.bodies:
                b.linear_velocity = 0, 0, 0
                b.angular_velocity = 0, 0, 0
        return states