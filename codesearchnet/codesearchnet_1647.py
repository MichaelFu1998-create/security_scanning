def _initEncoder(self, w, minval, maxval, n, radius, resolution):
    """ (helper function)  There are three different ways of thinking about the representation.
     Handle each case here."""
    if n != 0:
      if (radius !=0 or resolution != 0):
        raise ValueError("Only one of n/radius/resolution can be specified for a ScalarEncoder")
      assert n > w
      self.n = n

      if (minval is not None and maxval is not None):
        if not self.periodic:
          self.resolution = float(self.rangeInternal) / (self.n - self.w)
        else:
          self.resolution = float(self.rangeInternal) / (self.n)

        self.radius = self.w * self.resolution

        if self.periodic:
          self.range = self.rangeInternal
        else:
          self.range = self.rangeInternal + self.resolution

    else:
      if radius != 0:
        if (resolution != 0):
          raise ValueError("Only one of radius/resolution can be specified for a ScalarEncoder")
        self.radius = radius
        self.resolution = float(self.radius) / w
      elif resolution != 0:
        self.resolution = float(resolution)
        self.radius = self.resolution * self.w
      else:
        raise Exception("One of n, radius, resolution must be specified for a ScalarEncoder")

      if (minval is not None and maxval is not None):
        if self.periodic:
          self.range = self.rangeInternal
        else:
          self.range = self.rangeInternal + self.resolution

        nfloat = self.w * (self.range / self.radius) + 2 * self.padding
        self.n = int(math.ceil(nfloat))