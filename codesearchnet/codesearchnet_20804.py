def join_to(self, joint, other_body=None, **kwargs):
        '''Connect this body to another one using a joint.

        This method creates a joint to fasten this body to the other one. See
        :func:`World.join`.

        Parameters
        ----------
        joint : str
            The type of joint to use when connecting these bodies.
        other_body : :class:`Body` or str, optional
            The other body to join with this one. If not given, connects this
            body to the world.
        '''
        self.world.join(joint, self, other_body, **kwargs)