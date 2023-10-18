def inverse_dynamics(self, angles, start=0, end=1e100, states=None, max_force=100):
        '''Follow a set of angle data, yielding dynamic joint torques.

        Parameters
        ----------
        angles : ndarray (num-frames x num-dofs)
            Follow angle data provided by this array of angle values.
        start : int, optional
            Start following angle data after this frame. Defaults to the start
            of the angle data.
        end : int, optional
            Stop following angle data after this frame. Defaults to the end of
            the angle data.
        states : list of body states, optional
            If given, set the states of the skeleton bodies to these values
            before starting to follow the marker data.
        max_force : float, optional
            Allow each degree of freedom in the skeleton to exert at most this
            force when attempting to follow the given joint angles. Defaults to
            100N. Setting this value to be large results in more accurate
            following but can cause oscillations in the PID controllers,
            resulting in noisy torques.

        Returns
        -------
        torques : sequence of torque frames
            Returns a generator of joint torque data for the skeleton. One set
            of joint torques will be generated for each frame of angle data
            between `start` and `end`.
        '''
        if states is not None:
            self.skeleton.set_body_states(states)

        for frame_no, frame in enumerate(angles):
            if frame_no < start:
                continue
            if frame_no >= end:
                break

            self.ode_space.collide(None, self.on_collision)

            states = self.skeleton.get_body_states()
            self.skeleton.set_body_states(states)

            # joseph's stability fix: step to compute torques, then reset the
            # skeleton to the start of the step, and then step using computed
            # torques. thus any numerical errors between the body states after
            # stepping using angle constraints will be removed, because we
            # will be stepping the model using the computed torques.

            self.skeleton.enable_motors(max_force)
            self.skeleton.set_target_angles(angles[frame_no])
            self.ode_world.step(self.dt)
            torques = self.skeleton.joint_torques
            self.skeleton.disable_motors()

            self.skeleton.set_body_states(states)
            self.skeleton.add_torques(torques)
            yield torques
            self.ode_world.step(self.dt)

            self.ode_contactgroup.empty()