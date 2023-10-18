def load_asf(self, source, **kwargs):
        '''Load a skeleton definition from an ASF text file.

        Parameters
        ----------
        source : str or file
            A filename or file-like object that contains text information
            describing a skeleton, in ASF format.
        '''
        if hasattr(source, 'read'):
            p = parser.parse_asf(source, self.world, self.jointgroup, **kwargs)
        else:
            with open(source) as handle:
                p = parser.parse_asf(handle, self.world, self.jointgroup, **kwargs)
        self.bodies = p.bodies
        self.joints = p.joints
        self.set_pid_params(kp=0.999 / self.world.dt)