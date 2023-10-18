def set_target_angles(self, angles):
        '''Move each joint toward a target angle.

        This method uses a PID controller to set a target angular velocity for
        each degree of freedom in the skeleton, based on the difference between
        the current and the target angle for the respective DOF.

        PID parameters are by default set to achieve a tiny bit less than
        complete convergence in one time step, using only the P term (i.e., the
        P coefficient is set to 1 - \delta, while I and D coefficients are set
        to 0). PID parameters can be updated by calling the `set_pid_params`
        method.

        Parameters
        ----------
        angles : list of float
            A list of the target angles for every joint in the skeleton.
        '''
        j = 0
        for joint in self.joints:
            velocities = [
                ctrl(tgt - cur, self.world.dt) for cur, tgt, ctrl in
                zip(joint.angles, angles[j:j+joint.ADOF], joint.controllers)]
            joint.velocities = velocities
            j += joint.ADOF