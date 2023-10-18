def _fire(self, layers, the_plot):
    """Launches a new bolt from a random Marauder."""
    # We don't fire if another Marauder fired a bolt just now.
    if the_plot.get('last_marauder_shot') == the_plot.frame: return
    the_plot['last_marauder_shot'] = the_plot.frame
    # Which Marauder should fire the laser bolt?
    col = np.random.choice(np.nonzero(layers['X'].sum(axis=0))[0])
    row = np.nonzero(layers['X'][:, col])[0][-1] + 1
    # Move ourselves just below that Marauder.
    self._teleport((row, col))