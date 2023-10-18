def join(self, shape, body_a, body_b=None, name=None, **kwargs):
        '''Create a new joint that connects two bodies together.

        Parameters
        ----------
        shape : str
            The "shape" of the joint to use for joining together two bodies.
            This should name a type of joint, such as "ball" or "piston".
        body_a : str or :class:`Body`
            The first body to join together with this joint. If a string is
            given, it will be used as the name of a body to look up in the
            world.
        body_b : str or :class:`Body`, optional
            If given, identifies the second body to join together with
            ``body_a``. If not given, ``body_a`` is joined to the world.
        name : str, optional
            If given, use this name for the created joint. If not given, a name
            will be constructed of the form
            "{body_a.name}^{shape}^{body_b.name}".

        Returns
        -------
        joint : :class:`Joint`
            The joint object that was created.
        '''
        ba = self.get_body(body_a)
        bb = self.get_body(body_b)
        shape = shape.lower()
        if name is None:
            name = '{}^{}^{}'.format(ba.name, shape, bb.name if bb else '')
        self._joints[name] = Joint.build(
            shape, name, self, body_a=ba, body_b=bb, **kwargs)
        return self._joints[name]