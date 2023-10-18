def ResetSection(self, directive):
    """Reset section checking for preprocessor directive.

    Args:
      directive: preprocessor directive (e.g. "if", "else").
    """
    # The name of the current section.
    self._section = self._INITIAL_SECTION
    # The path of last found header.
    self._last_header = ''

    # Update list of includes.  Note that we never pop from the
    # include list.
    if directive in ('if', 'ifdef', 'ifndef'):
      self.include_list.append([])
    elif directive in ('else', 'elif'):
      self.include_list[-1] = []