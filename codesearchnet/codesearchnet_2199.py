def _fly(self, board, layers, things, the_plot):
    """Handles the behaviour of visible bolts flying toward the player."""
    # Disappear if we've hit a bunker.
    if self.character in the_plot['bunker_hitters']:
      return self._teleport((-1, -1))
    # End the game if we've hit the player.
    if self.position == things['P'].position: the_plot.terminate_episode()
    self._south(board, the_plot)