def draw_graph(self, line_kwargs=None, scatter_kwargs=None, **kwargs):
        """Draws the graph.

        Uses matplotlib, specifically
        :class:`~matplotlib.collections.LineCollection` and
        :meth:`~matplotlib.axes.Axes.scatter`. Gets the default
        keyword arguments for both methods by calling
        :meth:`~.QueueNetworkDiGraph.lines_scatter_args` first.

        Parameters
        ----------
        line_kwargs : dict (optional, default: ``None``)
            Any keyword arguments accepted by
            :class:`~matplotlib.collections.LineCollection`
        scatter_kwargs : dict (optional, default: ``None``)
            Any keyword arguments accepted by
            :meth:`~matplotlib.axes.Axes.scatter`.
        bgcolor : list (optional, keyword only)
            A list with 4 floats representing a RGBA color. Defaults
            to ``[1, 1, 1, 1]``.
        figsize : tuple (optional, keyword only, default: ``(7, 7)``)
            The width and height of the figure in inches.
        kwargs :
            Any keyword arguments used by
            :meth:`~matplotlib.figure.Figure.savefig`.

        Raises
        ------
        ImportError :
            If Matplotlib is not installed then an :exc:`ImportError`
            is raised.

        Notes
        -----
        If the ``fname`` keyword is passed, then the figure is saved
        locally.
        """
        if not HAS_MATPLOTLIB:
            raise ImportError("Matplotlib is required to draw the graph.")

        fig = plt.figure(figsize=kwargs.get('figsize', (7, 7)))
        ax = fig.gca()

        mpl_kwargs = {
            'line_kwargs': line_kwargs,
            'scatter_kwargs': scatter_kwargs,
            'pos': kwargs.get('pos')
        }

        line_kwargs, scatter_kwargs = self.lines_scatter_args(**mpl_kwargs)

        edge_collection = LineCollection(**line_kwargs)
        ax.add_collection(edge_collection)
        ax.scatter(**scatter_kwargs)

        if hasattr(ax, 'set_facecolor'):
            ax.set_facecolor(kwargs.get('bgcolor', [1, 1, 1, 1]))
        else:
            ax.set_axis_bgcolor(kwargs.get('bgcolor', [1, 1, 1, 1]))

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        if 'fname' in kwargs:
            # savefig needs a positional argument for some reason
            new_kwargs = {k: v for k, v in kwargs.items() if k in SAVEFIG_KWARGS}
            fig.savefig(kwargs['fname'], **new_kwargs)
        else:
            plt.ion()
            plt.show()