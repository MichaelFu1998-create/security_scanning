def add_torque(self, torque, relative=False):
        '''Add a torque to this body.

        Parameters
        ----------
        force : 3-tuple of float
            A vector giving the torque along each world or body coordinate axis.
        relative : bool, optional
            If False, the torque values are assumed to be given in the world
            coordinate frame. If True, they are assumed to be given in the
            body-relative coordinate frame. Defaults to False.
        '''
        op = self.ode_body.addRelTorque if relative else self.ode_body.addTorque
        op(torque)