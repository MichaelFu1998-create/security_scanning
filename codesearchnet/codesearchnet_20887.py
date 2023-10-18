def inverse_kinematics(self, start=0, end=1e100, states=None, max_force=20):
        '''Follow a set of marker data, yielding kinematic joint angles.

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
        max_force : float, optional
            Allow each degree of freedom in the skeleton to exert at most this
            force when attempting to maintain its equilibrium position. This
            defaults to 20N. Set this value higher to simulate a stiff skeleton
            while following marker data.

        Returns
        -------
        angles : sequence of angle frames
            Returns a generator of joint angle data for the skeleton. One set of
            joint angles will be generated for each frame of marker data between
            `start` and `end`.
        '''
        zeros = None
        if max_force > 0:
            self.skeleton.enable_motors(max_force)
            zeros = np.zeros(self.skeleton.num_dofs)
        for _ in self.follow_markers(start, end, states):
            if zeros is not None:
                self.skeleton.set_target_angles(zeros)
            yield self.skeleton.joint_angles