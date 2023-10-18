def set_pid_params(self, *args, **kwargs):
        '''Set PID parameters for all joints in the skeleton.

        Parameters for this method are passed directly to the `pid` constructor.
        '''
        for joint in self.joints:
            joint.target_angles = [None] * joint.ADOF
            joint.controllers = [pid(*args, **kwargs) for i in range(joint.ADOF)]