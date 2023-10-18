def enable_motors(self, max_force):
        '''Enable the joint motors in this skeleton.

        This method sets the maximum force that can be applied by each joint to
        attain the desired target velocities. It also enables torque feedback
        for all joint motors.

        Parameters
        ----------
        max_force : float
            The maximum force that each joint is allowed to apply to attain its
            target velocity.
        '''
        for joint in self.joints:
            amotor = getattr(joint, 'amotor', joint)
            amotor.max_forces = max_force
            if max_force > 0:
                amotor.enable_feedback()
            else:
                amotor.disable_feedback()