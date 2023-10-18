def connect_to(self, joint, other_body, offset=(0, 0, 0), other_offset=(0, 0, 0),
                   **kwargs):
        '''Move another body next to this one and join them together.

        This method will move the ``other_body`` so that the anchor points for
        the joint coincide. It then creates a joint to fasten the two bodies
        together. See :func:`World.move_next_to` and :func:`World.join`.

        Parameters
        ----------
        joint : str
            The type of joint to use when connecting these bodies.
        other_body : :class:`Body` or str
            The other body to join with this one.
        offset : 3-tuple of float, optional
            The body-relative offset where the anchor for the joint should be
            placed. Defaults to (0, 0, 0). See :func:`World.move_next_to` for a
            description of how offsets are specified.
        other_offset : 3-tuple of float, optional
            The offset on the second body where the joint anchor should be
            placed. Defaults to (0, 0, 0). Like ``offset``, this is given as an
            offset relative to the size and shape of ``other_body``.
        '''
        anchor = self.world.move_next_to(self, other_body, offset, other_offset)
        self.world.join(joint, self, other_body, anchor=anchor, **kwargs)