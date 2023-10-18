def is_kinematic(self, is_kinematic):
        '''Set the kinematic/dynamic attribute for this body.

        In pagoda, kinematic bodies have infinite mass and do interact with
        other bodies via collisions.

        Parameters
        ----------
        is_kinematic : bool
            If True, this body will be set to kinematic. If False, it will be
            set to dynamic.
        '''
        if is_kinematic:
            self.ode_body.setKinematic()
        else:
            self.ode_body.setDynamic()