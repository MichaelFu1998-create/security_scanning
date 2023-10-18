def sim_matrix(
        src,
        tar,
        mat=None,
        mismatch_cost=0,
        match_cost=1,
        symmetric=True,
        alphabet=None,
    ):
        """Return the matrix similarity of two strings.

        With the default parameters, this is identical to sim_ident.
        It is possible for sim_matrix to return values outside of the range
        :math:`[0, 1]`, if values outside that range are present in mat,
        mismatch_cost, or match_cost.

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        mat : dict
            A dict mapping tuples to costs; the tuples are (src, tar) pairs of
            symbols from the alphabet parameter
        mismatch_cost : float
            The value returned if (src, tar) is absent from mat when src does
            not equal tar
        match_cost : float
            The value returned if (src, tar) is absent from mat when src equals
            tar
        symmetric : bool
            True if the cost of src not matching tar is identical to the cost
            of tar not matching src; in this case, the values in mat need only
            contain (src, tar) or (tar, src), not both
        alphabet : str
            A collection of tokens from which src and tar are drawn; if this is
            defined a ValueError is raised if either tar or src is not found in
            alphabet

        Returns
        -------
        float
            Matrix similarity

        Raises
        ------
        ValueError
            src value not in alphabet
        ValueError
            tar value not in alphabet

        Examples
        --------
        >>> NeedlemanWunsch.sim_matrix('cat', 'hat')
        0
        >>> NeedlemanWunsch.sim_matrix('hat', 'hat')
        1

        """
        if alphabet:
            alphabet = tuple(alphabet)
            for i in src:
                if i not in alphabet:
                    raise ValueError('src value not in alphabet')
            for i in tar:
                if i not in alphabet:
                    raise ValueError('tar value not in alphabet')

        if src == tar:
            if mat and (src, src) in mat:
                return mat[(src, src)]
            return match_cost
        if mat and (src, tar) in mat:
            return mat[(src, tar)]
        elif symmetric and mat and (tar, src) in mat:
            return mat[(tar, src)]
        return mismatch_cost