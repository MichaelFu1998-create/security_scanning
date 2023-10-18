def move_next_to(self, body_a, body_b, offset_a, offset_b):
        '''Move one body to be near another one.

        After moving, the location described by ``offset_a`` on ``body_a`` will
        be coincident with the location described by ``offset_b`` on ``body_b``.

        Parameters
        ----------
        body_a : str or :class:`Body`
            The body to use as a reference for moving the other body. If this is
            a string, it is treated as the name of a body to look up in the
            world.
        body_b : str or :class:`Body`
            The body to move next to ``body_a``. If this is a string, it is
            treated as the name of a body to look up in the world.
        offset_a : 3-tuple of float
            The offset of the anchor point, given as a relative fraction of the
            size of ``body_a``. See :func:`Body.relative_offset_to_world`.
        offset_b : 3-tuple of float
            The offset of the anchor point, given as a relative fraction of the
            size of ``body_b``.

        Returns
        -------
        anchor : 3-tuple of float
            The location of the shared point, which is often useful to use as a
            joint anchor.
        '''
        ba = self.get_body(body_a)
        bb = self.get_body(body_b)
        if ba is None:
            return bb.relative_offset_to_world(offset_b)
        if bb is None:
            return ba.relative_offset_to_world(offset_a)
        anchor = ba.relative_offset_to_world(offset_a)
        offset = bb.relative_offset_to_world(offset_b)
        bb.position = bb.position + anchor - offset
        return anchor