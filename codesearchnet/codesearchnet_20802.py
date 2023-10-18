def add_force(self, force, relative=False, position=None, relative_position=None):
        '''Add a force to this body.

        Parameters
        ----------
        force : 3-tuple of float
            A vector giving the forces along each world or body coordinate axis.
        relative : bool, optional
            If False, the force values are assumed to be given in the world
            coordinate frame. If True, they are assumed to be given in the
            body-relative coordinate frame. Defaults to False.
        position : 3-tuple of float, optional
            If given, apply the force at this location in world coordinates.
            Defaults to the current position of the body.
        relative_position : 3-tuple of float, optional
            If given, apply the force at this relative location on the body. If
            given, this method ignores the ``position`` parameter.
        '''
        b = self.ode_body
        if relative_position is not None:
            op = b.addRelForceAtRelPos if relative else b.addForceAtRelPos
            op(force, relative_position)
        elif position is not None:
            op = b.addRelForceAtPos if relative else b.addForceAtPos
            op(force, position)
        else:
            op = b.addRelForce if relative else b.addForce
            op(force)