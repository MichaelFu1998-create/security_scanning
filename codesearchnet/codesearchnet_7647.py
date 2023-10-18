def plot_time_freq(self, mindB=-100, maxdB=None, norm=True,
            yaxis_label_position="right"):
        """Plotting method to plot both time and frequency domain results.

        See :meth:`plot_frequencies` for the optional arguments.

        .. plot::
            :width: 80%
            :include-source:

            from spectrum.window import Window
            w = Window(64, name='hamming')
            w.plot_time_freq()

        """
        from pylab import subplot, gca

        subplot(1, 2, 1)
        self.plot_window()

        subplot(1, 2, 2)
        self.plot_frequencies(mindB=mindB, maxdB=maxdB, norm=norm)

        if yaxis_label_position=="left":
            try: tight_layout()
            except: pass
        else:
            ax = gca()
            ax.yaxis.set_label_position("right")