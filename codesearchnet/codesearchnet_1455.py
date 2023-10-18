def agitate(self):
    """Agitate this particle so that it is likely to go to a new position.
    Every time agitate is called, the particle is jiggled an even greater
    amount.

    Parameters:
    --------------------------------------------------------------
    retval:               None
    """
    for (varName, var) in self.permuteVars.iteritems():
      var.agitate()

    self.newPosition()