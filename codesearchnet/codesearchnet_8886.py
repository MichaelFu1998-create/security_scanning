def lines_scatter_args(self, line_kwargs=None, scatter_kwargs=None, pos=None):
        """Returns the arguments used when plotting.

        Takes any keyword arguments for
        :class:`~matplotlib.collections.LineCollection` and
        :meth:`~matplotlib.axes.Axes.scatter` and returns two
        dictionaries with all the defaults set.

        Parameters
        ----------
        line_kwargs : dict (optional, default: ``None``)
            Any keyword arguments accepted by
            :class:`~matplotlib.collections.LineCollection`.
        scatter_kwargs : dict (optional, default: ``None``)
            Any keyword arguments accepted by
            :meth:`~matplotlib.axes.Axes.scatter`.

        Returns
        -------
        tuple
            A 2-tuple of dicts. The first entry is the keyword
            arguments for
            :class:`~matplotlib.collections.LineCollection` and the
            second is the keyword args for
            :meth:`~matplotlib.axes.Axes.scatter`.

        Notes
        -----
        If a specific keyword argument is not passed then the defaults
        are used.
        """
        if pos is not None:
            self.set_pos(pos)
        elif self.pos is None:
            self.set_pos()

        edge_pos = [0 for e in self.edges()]
        for e in self.edges():
            ei = self.edge_index[e]
            edge_pos[ei] = (self.pos[e[0]], self.pos[e[1]])

        line_collecton_kwargs = {
            'segments': edge_pos,
            'colors': self.edge_color,
            'linewidths': (1,),
            'antialiaseds': (1,),
            'linestyle': 'solid',
            'transOffset': None,
            'cmap': plt.cm.ocean_r,
            'pickradius': 5,
            'zorder': 0,
            'facecolors': None,
            'norm': None,
            'offsets': None,
            'offset_position': 'screen',
            'hatch': None,
        }
        scatter_kwargs_ = {
            'x': self.pos[:, 0],
            'y': self.pos[:, 1],
            's': 50,
            'c': self.vertex_fill_color,
            'alpha': None,
            'norm': None,
            'vmin': None,
            'vmax': None,
            'marker': 'o',
            'zorder': 2,
            'cmap': plt.cm.ocean_r,
            'linewidths': 1,
            'edgecolors': self.vertex_color,
            'facecolors': None,
            'antialiaseds': None,
            'offset_position': 'screen',
            'hatch': None,
        }

        line_kwargs = {} if line_kwargs is None else line_kwargs
        scatter_kwargs = {} if scatter_kwargs is None else scatter_kwargs

        for key, value in line_kwargs.items():
            if key in line_collecton_kwargs:
                line_collecton_kwargs[key] = value

        for key, value in scatter_kwargs.items():
            if key in scatter_kwargs_:
                scatter_kwargs_[key] = value

        return line_collecton_kwargs, scatter_kwargs_