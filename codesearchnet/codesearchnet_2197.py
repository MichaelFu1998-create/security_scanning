def _fly(self, board, layers, things, the_plot):
    """Handles the behaviour of visible bolts flying toward Marauders."""
    # Disappear if we've hit a Marauder or a bunker.
    if (self.character in the_plot['bunker_hitters'] or
        self.character in the_plot['marauder_hitters']):
      return self._teleport((-1, -1))
    # Otherwise, northward!
    self._north(board, the_plot)