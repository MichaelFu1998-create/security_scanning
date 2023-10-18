def sim(self, src, tar, qval=2, alpha=1, beta=1, bias=None):
        """Return the Tversky index of two strings.

        Parameters
        ----------
        src : str
            Source string (or QGrams/Counter objects) for comparison
        tar : str
            Target string (or QGrams/Counter objects) for comparison
        qval : int
            The length of each q-gram; 0 for non-q-gram version
        alpha : float
            Tversky index parameter as described above
        beta : float
            Tversky index parameter as described above
        bias : float
            The symmetric Tversky index bias parameter

        Returns
        -------
        float
            Tversky similarity

        Raises
        ------
        ValueError
            Unsupported weight assignment; alpha and beta must be greater than
            or equal to 0.

        Examples
        --------
        >>> cmp = Tversky()
        >>> cmp.sim('cat', 'hat')
        0.3333333333333333
        >>> cmp.sim('Niall', 'Neil')
        0.2222222222222222
        >>> cmp.sim('aluminum', 'Catalan')
        0.0625
        >>> cmp.sim('ATCG', 'TAGC')
        0.0

        """
        if alpha < 0 or beta < 0:
            raise ValueError(
                'Unsupported weight assignment; alpha and beta '
                + 'must be greater than or equal to 0.'
            )

        if src == tar:
            return 1.0
        elif not src or not tar:
            return 0.0

        q_src, q_tar = self._get_qgrams(src, tar, qval)
        q_src_mag = sum(q_src.values())
        q_tar_mag = sum(q_tar.values())
        q_intersection_mag = sum((q_src & q_tar).values())

        if not q_src or not q_tar:
            return 0.0

        if bias is None:
            return q_intersection_mag / (
                q_intersection_mag
                + alpha * (q_src_mag - q_intersection_mag)
                + beta * (q_tar_mag - q_intersection_mag)
            )

        a_val = min(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        b_val = max(
            q_src_mag - q_intersection_mag, q_tar_mag - q_intersection_mag
        )
        c_val = q_intersection_mag + bias
        return c_val / (beta * (alpha * a_val + (1 - alpha) * b_val) + c_val)