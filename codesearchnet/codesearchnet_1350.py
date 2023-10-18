def inferRowCompat(self, distribution):
    """
    Equivalent to the category inference of zeta1.TopLevel.
    Computes the max_prod (maximum component of a component-wise multiply)
    between the rows of the histogram and the incoming distribution.
    May be slow if the result of clean_outcpd() is not valid.

    :param distribution: Array of length equal to the number of columns.
    :returns: array of length equal to the number of rows.
    """
    if self.hack_ is None:
      self.clean_outcpd()
    return self.hack_.vecMaxProd(distribution)