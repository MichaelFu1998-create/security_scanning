def draw(self, update_colors=True, line_kwargs=None,
             scatter_kwargs=None, **kwargs):
        """Draws the network. The coloring of the network corresponds
        to the number of agents at each queue.

        Parameters
        ----------
        update_colors : ``bool`` (optional, default: ``True``).
            Specifies whether all the colors are updated.
        line_kwargs : dict (optional, default: None)
            Any keyword arguments accepted by
            :class:`~matplotlib.collections.LineCollection`
        scatter_kwargs : dict (optional, default: None)
            Any keyword arguments accepted by
            :meth:`~matplotlib.axes.Axes.scatter`.
        bgcolor : list (optional, keyword only)
            A list with 4 floats representing a RGBA color. The
            default is defined in ``self.colors['bgcolor']``.
        figsize : tuple (optional, keyword only, default: ``(7, 7)``)
            The width and height of the canvas in inches.
        **kwargs
            Any parameters to pass to
            :meth:`.QueueNetworkDiGraph.draw_graph`.

        Notes
        -----
        This method relies heavily on
        :meth:`.QueueNetworkDiGraph.draw_graph`. Also, there is a
        parameter that sets the background color of the canvas, which
        is the ``bgcolor`` parameter.

        Examples
        --------
        To draw the current state of the network, call:

        >>> import queueing_tool as qt
        >>> g = qt.generate_pagerank_graph(100, seed=13)
        >>> net = qt.QueueNetwork(g, seed=13)
        >>> net.initialize(100)
        >>> net.simulate(1200)
        >>> net.draw() # doctest: +SKIP

        If you specify a file name and location, the drawing will be
        saved to disk. For example, to save the drawing to the current
        working directory do the following:

        >>> net.draw(fname="state.png", scatter_kwargs={'s': 40}) # doctest: +SKIP

        .. figure:: current_state1.png
            :align: center

        The shade of each edge depicts how many agents are located at
        the corresponding queue. The shade of each vertex is determined
        by the total number of inbound agents. Although loops are not
        visible by default, the vertex that corresponds to a loop shows
        how many agents are in that loop.

        There are several additional parameters that can be passed --
        all :meth:`.QueueNetworkDiGraph.draw_graph` parameters are
        valid. For example, to show the edges as dashed lines do the
        following.

        >>> net.draw(line_kwargs={'linestyle': 'dashed'}) # doctest: +SKIP
        """
        if not HAS_MATPLOTLIB:
            raise ImportError("matplotlib is necessary to draw the network.")

        if update_colors:
            self._update_all_colors()

        if 'bgcolor' not in kwargs:
            kwargs['bgcolor'] = self.colors['bgcolor']

        self.g.draw_graph(line_kwargs=line_kwargs,
                          scatter_kwargs=scatter_kwargs, **kwargs)