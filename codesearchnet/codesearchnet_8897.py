def animate(self, out=None, t=None, line_kwargs=None,
                scatter_kwargs=None, **kwargs):
        """Animates the network as it's simulating.

        The animations can be saved to disk or viewed in interactive
        mode. Closing the window ends the animation if viewed in
        interactive mode. This method calls
        :meth:`~matplotlib.axes.scatter`, and
        :class:`~matplotlib.collections.LineCollection`, and any
        keyword arguments they accept can be passed to them.

        Parameters
        ----------
        out : str (optional)
            The location where the frames for the images will be saved.
            If this parameter is not given, then the animation is shown
            in interactive mode.
        t : float (optional)
            The amount of simulation time to simulate forward. If
            given, and ``out`` is given, ``t`` is used instead of
            ``n``.
        line_kwargs : dict (optional, default: None)
            Any keyword arguments accepted by
            :class:`~matplotlib.collections.LineCollection`.
        scatter_kwargs : dict (optional, default: None)
            Any keyword arguments accepted by
            :meth:`~matplotlib.axes.Axes.scatter`.
        bgcolor : list (optional, keyword only)
            A list with 4 floats representing a RGBA color. The
            default is defined in ``self.colors['bgcolor']``.
        figsize : tuple (optional, keyword only, default: ``(7, 7)``)
            The width and height of the figure in inches.
        **kwargs :
            This method calls
            :class:`~matplotlib.animation.FuncAnimation` and
            optionally :meth:`.matplotlib.animation.FuncAnimation.save`.
            Any keyword that can be passed to these functions are
            passed via ``kwargs``.

        Notes
        -----
        There are several parameters automatically set and passed to
        matplotlib's :meth:`~matplotlib.axes.Axes.scatter`,
        :class:`~matplotlib.collections.LineCollection`, and
        :class:`~matplotlib.animation.FuncAnimation` by default.
        These include:

            * :class:`~matplotlib.animation.FuncAnimation`: Uses the
              defaults for that function. Saving the animation is done
              by passing the 'filename' keyword argument to this method.
              This method also accepts any keyword arguments accepted
              by :meth:`~matplotlib.animation.FuncAnimation.save`.
            * :class:`~matplotlib.collections.LineCollection`: The default
              arguments are taken from
              :meth:`.QueueNetworkDiGraph.lines_scatter_args`.
            * :meth:`~matplotlib.axes.Axes.scatter`: The default
              arguments are taken from
              :meth:`.QueueNetworkDiGraph.lines_scatter_args`.

        Raises
        ------
        QueueingToolError
            Will raise a :exc:`.QueueingToolError` if the
            ``QueueNetwork`` has not been initialized. Call
            :meth:`.initialize` before running.

        Examples
        --------
        This function works similarly to ``QueueNetwork's``
        :meth:`.draw` method.

        >>> import queueing_tool as qt
        >>> g = qt.generate_pagerank_graph(100, seed=13)
        >>> net = qt.QueueNetwork(g, seed=13)
        >>> net.initialize()
        >>> net.animate(figsize=(4, 4)) # doctest: +SKIP

        To stop the animation just close the window. If you want to
        write the animation to disk run something like the following:

        >>> kwargs = {
        ...     'filename': 'test.mp4',
        ...     'frames': 300,
        ...     'fps': 30,
        ...     'writer': 'mencoder',
        ...     'figsize': (4, 4),
        ...     'vertex_size': 15
        ... }
        >>> net.animate(**kwargs) # doctest: +SKIP
        """

        if not self._initialized:
            msg = ("Network has not been initialized. "
                   "Call '.initialize()' first.")
            raise QueueingToolError(msg)

        if not HAS_MATPLOTLIB:
            msg = "Matplotlib is necessary to animate a simulation."
            raise ImportError(msg)

        self._update_all_colors()
        kwargs.setdefault('bgcolor', self.colors['bgcolor'])

        fig = plt.figure(figsize=kwargs.get('figsize', (7, 7)))
        ax = fig.gca()

        mpl_kwargs = {
            'line_kwargs': line_kwargs,
            'scatter_kwargs': scatter_kwargs,
            'pos': kwargs.get('pos')
        }

        line_args, scat_args = self.g.lines_scatter_args(**mpl_kwargs)

        lines = LineCollection(**line_args)
        lines = ax.add_collection(lines)
        scatt = ax.scatter(**scat_args)

        t = np.infty if t is None else t
        now = self._t

        def update(frame_number):
            if t is not None:
                if self._t > now + t:
                    return False
            self._simulate_next_event(slow=True)
            lines.set_color(line_args['colors'])
            scatt.set_edgecolors(scat_args['edgecolors'])
            scatt.set_facecolor(scat_args['c'])

        if hasattr(ax, 'set_facecolor'):
            ax.set_facecolor(kwargs['bgcolor'])
        else:
            ax.set_axis_bgcolor(kwargs['bgcolor'])

        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        animation_args = {
            'fargs': None,
            'event_source': None,
            'init_func': None,
            'frames': None,
            'blit': False,
            'interval': 10,
            'repeat': None,
            'func': update,
            'repeat_delay': None,
            'fig': fig,
            'save_count': None,
        }
        for key, value in kwargs.items():
            if key in animation_args:
                animation_args[key] = value

        animation = FuncAnimation(**animation_args)
        if 'filename' not in kwargs:
            plt.ioff()
            plt.show()
        else:
            save_args = {
                'filename': None,
                'writer': None,
                'fps': None,
                'dpi': None,
                'codec': None,
                'bitrate': None,
                'extra_args': None,
                'metadata': None,
                'extra_anim': None,
                'savefig_kwargs': None
            }
            for key, value in kwargs.items():
                if key in save_args:
                    save_args[key] = value

            animation.save(**save_args)