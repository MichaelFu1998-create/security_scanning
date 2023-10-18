def _fire(self, layers, things, the_plot):
    """Launches a new bolt from the player."""
    # We don't fire if the player fired another bolt just now.
    if the_plot.get('last_player_shot') == the_plot.frame: return
    the_plot['last_player_shot'] = the_plot.frame
    # We start just above the player.
    row, col = things['P'].position
    self._teleport((row-1, col))