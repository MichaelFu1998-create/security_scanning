def load_skeleton(self, filename, pid_params=None):
        '''Create and configure a skeleton in our model.

        Parameters
        ----------
        filename : str
            The name of a file containing skeleton configuration data.
        pid_params : dict, optional
            If given, use this dictionary to set the PID controller
            parameters on each joint in the skeleton. See
            :func:`pagoda.skeleton.pid` for more information.
        '''
        self.skeleton = skeleton.Skeleton(self)
        self.skeleton.load(filename, color=(0.3, 0.5, 0.9, 0.8))
        if pid_params:
            self.skeleton.set_pid_params(**pid_params)
        self.skeleton.erp = 0.1
        self.skeleton.cfm = 0