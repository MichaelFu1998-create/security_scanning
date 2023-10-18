def FindHeader(self, header):
    """Check if a header has already been included.

    Args:
      header: header to check.
    Returns:
      Line number of previous occurrence, or -1 if the header has not
      been seen before.
    """
    for section_list in self.include_list:
      for f in section_list:
        if f[0] == header:
          return f[1]
    return -1