def plot_frequencies(self, mindB=None, maxdB=None, norm=True):
        """Plot the window in the frequency domain

        :param mindB: change the default lower y bound
        :param maxdB: change the default upper lower bound
        :param bool norm: if True, normalise the frequency response.

        .. plot::
            :width: 80%
            :include-source:

            from spectrum.window import Window
            w = Window(64, name='hamming')
            w.plot_frequencies()

        """
        from pylab import plot, title, xlim, grid, ylim, xlabel, ylabel
        # recompute the response
        self.compute_response(norm=norm)

        plot(self.frequencies, self.response)
        title("ENBW=%2.1f" % (self.enbw))
        ylabel('Frequency response (dB)')
        xlabel('Fraction of sampling frequency')
        # define the plot limits
        xlim(-0.5, 0.5)
        y0, y1 = ylim()
        if mindB:
            y0 = mindB
        if maxdB is not None:
            y1 = maxdB
        else:
            y1 = max(self.response)

        ylim(y0, y1)

        grid(True)