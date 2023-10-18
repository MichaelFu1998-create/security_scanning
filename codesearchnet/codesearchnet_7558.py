def plot(self, **kargs):
        """Plot the data set, using the sampling information to set the x-axis
        correctly."""
        from pylab import plot, linspace, xlabel, ylabel, grid
        time = linspace(1*self.dt, self.N*self.dt, self.N)
        plot(time, self.data, **kargs)
        xlabel('Time')
        ylabel('Amplitude')
        grid(True)