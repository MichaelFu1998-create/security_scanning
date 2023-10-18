def plot_window(self):
        """Plot the window in the time domain

        .. plot::
            :width: 80%
            :include-source:

            from spectrum.window import Window
            w = Window(64, name='hamming')
            w.plot_window()

        """
        from pylab import plot, xlim, grid, title, ylabel, axis
        x = linspace(0, 1, self.N)
        xlim(0, 1)
        plot(x, self.data)
        grid(True)
        title('%s Window (%s points)' % (self.name.capitalize(), self.N))
        ylabel('Amplitude')
        axis([0, 1, 0, 1.1])