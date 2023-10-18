def dist(
        self,
        src,
        tar,
        metric='euclidean',
        cost=(1, 1, 0.5, 0.5),
        layout='QWERTY',
    ):
        """Return the normalized typo distance between two strings.

        This is typo distance, normalized to [0, 1].

        Parameters
        ----------
        src : str
            Source string for comparison
        tar : str
            Target string for comparison
        metric : str
            Supported values include: ``euclidean``, ``manhattan``,
            ``log-euclidean``, and ``log-manhattan``
        cost : tuple
            A 4-tuple representing the cost of the four possible edits:
            inserts, deletes, substitutions, and shift, respectively (by
            default: (1, 1, 0.5, 0.5)) The substitution & shift costs should be
            significantly less than the cost of an insertion & deletion unless
            a log metric is used.
        layout : str
            Name of the keyboard layout to use (Currently supported:
            ``QWERTY``, ``Dvorak``, ``AZERTY``, ``QWERTZ``)

        Returns
        -------
        float
            Normalized typo distance

        Examples
        --------
        >>> cmp = Typo()
        >>> round(cmp.dist('cat', 'hat'), 12)
        0.527046283086
        >>> round(cmp.dist('Niall', 'Neil'), 12)
        0.565028142929
        >>> round(cmp.dist('Colin', 'Cuilen'), 12)
        0.569035609563
        >>> cmp.dist('ATCG', 'TAGC')
        0.625

        """
        if src == tar:
            return 0.0
        ins_cost, del_cost = cost[:2]
        return self.dist_abs(src, tar, metric, cost, layout) / (
            max(len(src) * del_cost, len(tar) * ins_cost)
        )