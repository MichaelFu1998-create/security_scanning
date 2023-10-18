def load_skel(self, source, **kwargs):
        '''Load a skeleton definition from a text file.

        Parameters
        ----------
        source : str or file
            A filename or file-like object that contains text information
            describing a skeleton. See :class:`pagoda.parser.BodyParser` for
            more information about the format of the text file.
        '''
        logging.info('%s: parsing skeleton configuration', source)
        if hasattr(source, 'read'):
            p = parser.parse(source, self.world, self.jointgroup, **kwargs)
        else:
            with open(source) as handle:
                p = parser.parse(handle, self.world, self.jointgroup, **kwargs)
        self.bodies = p.bodies
        self.joints = p.joints
        self.set_pid_params(kp=0.999 / self.world.dt)