def set_transitions(self, mat):
        """Change the routing transitions probabilities for the
        network.

        Parameters
        ----------
        mat : dict or :class:`~numpy.ndarray`
            A transition routing matrix or transition dictionary. If
            passed a dictionary, the keys are source vertex indices and
            the values are dictionaries with target vertex indicies
            as the keys and the probabilities of routing from the
            source to the target as the values.

        Raises
        ------
        ValueError
            A :exc:`.ValueError` is raised if: the keys in the dict
            don't match with a vertex index in the graph; or if the
            :class:`~numpy.ndarray` is passed with the wrong shape,
            must be (``num_vertices``, ``num_vertices``); or the values
            passed are not probabilities (for each vertex they are
            positive and sum to 1);
        TypeError
            A :exc:`.TypeError` is raised if mat is not a dict or
            :class:`~numpy.ndarray`.

        Examples
        --------
        The default transition matrix is every out edge being equally
        likely:

        >>> import queueing_tool as qt
        >>> adjacency = {
        ...     0: [2],
        ...     1: [2, 3],
        ...     2: [0, 1, 2, 4],
        ...     3: [1],
        ...     4: [2],
        ... }
        >>> g = qt.adjacency2graph(adjacency)
        >>> net = qt.QueueNetwork(g)
        >>> net.transitions(False)  # doctest: +ELLIPSIS
        ...                         # doctest: +NORMALIZE_WHITESPACE
        {0: {2: 1.0},
         1: {2: 0.5, 3: 0.5},
         2: {0: 0.25, 1: 0.25, 2: 0.25, 4: 0.25},
         3: {1: 1.0},
         4: {2: 1.0}}

        If you want to change only one vertex's transition
        probabilities, you can do so with the following:

        >>> net.set_transitions({1 : {2: 0.75, 3: 0.25}})
        >>> net.transitions(False)  # doctest: +ELLIPSIS
        ...                         # doctest: +NORMALIZE_WHITESPACE
        {0: {2: 1.0},
         1: {2: 0.75, 3: 0.25},
         2: {0: 0.25, 1: 0.25, 2: 0.25, 4: 0.25},
         3: {1: 1.0},
         4: {2: 1.0}}

        One can generate a transition matrix using
        :func:`.generate_transition_matrix`. You can change all
        transition probabilities with an :class:`~numpy.ndarray`:

        >>> mat = qt.generate_transition_matrix(g, seed=10)
        >>> net.set_transitions(mat)
        >>> net.transitions(False)  # doctest: +ELLIPSIS
        ...                         # doctest: +NORMALIZE_WHITESPACE
        {0: {2: 1.0},
         1: {2: 0.962..., 3: 0.037...},
         2: {0: 0.301..., 1: 0.353..., 2: 0.235..., 4: 0.108...},
         3: {1: 1.0},
         4: {2: 1.0}}

        See Also
        --------
        :meth:`.transitions` : Return the current routing
            probabilities.
        :func:`.generate_transition_matrix` : Generate a random routing
            matrix.
        """
        if isinstance(mat, dict):
            for key, value in mat.items():
                probs = list(value.values())

                if key not in self.g.node:
                    msg = "One of the keys don't correspond to a vertex."
                    raise ValueError(msg)
                elif len(self.out_edges[key]) > 0 and not np.isclose(sum(probs), 1):
                    msg = "Sum of transition probabilities at a vertex was not 1."
                    raise ValueError(msg)
                elif (np.array(probs) < 0).any():
                    msg = "Some transition probabilities were negative."
                    raise ValueError(msg)

                for k, e in enumerate(sorted(self.g.out_edges(key))):
                    self._route_probs[key][k] = value.get(e[1], 0)

        elif isinstance(mat, np.ndarray):
            non_terminal = np.array([self.g.out_degree(v) > 0 for v in self.g.nodes()])
            if mat.shape != (self.nV, self.nV):
                msg = ("Matrix is the wrong shape, should "
                       "be {0} x {1}.").format(self.nV, self.nV)
                raise ValueError(msg)
            elif not np.allclose(np.sum(mat[non_terminal, :], axis=1), 1):
                msg = "Sum of transition probabilities at a vertex was not 1."
                raise ValueError(msg)
            elif (mat < 0).any():
                raise ValueError("Some transition probabilities were negative.")

            for k in range(self.nV):
                for j, e in enumerate(sorted(self.g.out_edges(k))):
                    self._route_probs[k][j] = mat[k, e[1]]
        else:
            raise TypeError("mat must be a numpy array or a dict.")