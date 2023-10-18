def make_game():
  """Builds and returns an Extraterrestrial Marauders game."""
  return ascii_art.ascii_art_to_game(
      GAME_ART, what_lies_beneath=' ',
      sprites=dict(
          [('P', PlayerSprite)] +
          [(c, UpwardLaserBoltSprite) for c in UPWARD_BOLT_CHARS] +
          [(c, DownwardLaserBoltSprite) for c in DOWNWARD_BOLT_CHARS]),
      drapes=dict(X=MarauderDrape,
                  B=BunkerDrape),
      update_schedule=['P', 'B', 'X'] + list(_ALL_BOLT_CHARS))