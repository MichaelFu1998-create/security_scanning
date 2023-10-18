def _setEncoderParams(self):
    """
    Set the radius, resolution and range. These values are updated when minval
    and/or maxval change.
    """

    self.rangeInternal = float(self.maxval - self.minval)

    self.resolution = float(self.rangeInternal) / (self.n - self.w)
    self.radius = self.w * self.resolution
    self.range = self.rangeInternal + self.resolution

    # nInternal represents the output area excluding the possible padding on each side
    self.nInternal = self.n - 2 * self.padding

    # Invalidate the bucket values cache so that they get recomputed
    self._bucketValues = None