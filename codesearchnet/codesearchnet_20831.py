def on_collision(self, args, geom_a, geom_b):
        '''Callback function for the collide() method.

        Parameters
        ----------
        args : None
            Arguments passed when the callback was registered. Not used.
        geom_a : ODE geometry
            The geometry object of one of the bodies that has collided.
        geom_b : ODE geometry
            The geometry object of one of the bodies that has collided.
        '''
        body_a = geom_a.getBody()
        body_b = geom_b.getBody()
        if ode.areConnected(body_a, body_b) or \
           (body_a and body_a.isKinematic()) or \
           (body_b and body_b.isKinematic()):
            return
        for c in ode.collide(geom_a, geom_b):
            c.setBounce(self.elasticity)
            c.setMu(self.friction)
            ode.ContactJoint(self.ode_world, self.ode_contactgroup, c).attach(
                geom_a.getBody(), geom_b.getBody())