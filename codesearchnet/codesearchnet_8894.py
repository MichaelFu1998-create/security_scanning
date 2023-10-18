def set_num_servers(self, n):
        """Change the number of servers in the queue to ``n``.

        Parameters
        ----------
        n : int or :const:`numpy.infty`
            A positive integer (or ``numpy.infty``) to set the number
            of queues in the system to.

        Raises
        ------
        TypeError
            If ``n`` is not an integer or positive infinity then this
            error is raised.
        ValueError
            If ``n`` is not positive.
        """
        if not isinstance(n, numbers.Integral) and n is not infty:
            the_str = "n must be an integer or infinity.\n{0}"
            raise TypeError(the_str.format(str(self)))
        elif n <= 0:
            the_str = "n must be a positive integer or infinity.\n{0}"
            raise ValueError(the_str.format(str(self)))
        else:
            self.num_servers = n