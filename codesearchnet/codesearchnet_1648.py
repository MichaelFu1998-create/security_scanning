def _getFirstOnBit(self, input):
    """ Return the bit offset of the first bit to be set in the encoder output.
    For periodic encoders, this can be a negative number when the encoded output
    wraps around. """

    if input == SENTINEL_VALUE_FOR_MISSING_DATA:
      return [None]

    else:
      if input < self.minval:
        # Don't clip periodic inputs. Out-of-range input is always an error
        if self.clipInput and not self.periodic:
          if self.verbosity > 0:
            print "Clipped input %s=%.2f to minval %.2f" % (self.name, input,
                                                            self.minval)
          input = self.minval
        else:
          raise Exception('input (%s) less than range (%s - %s)' %
                          (str(input), str(self.minval), str(self.maxval)))

      if self.periodic:
        # Don't clip periodic inputs. Out-of-range input is always an error
        if input >= self.maxval:
          raise Exception('input (%s) greater than periodic range (%s - %s)' %
                          (str(input), str(self.minval), str(self.maxval)))
      else:
        if input > self.maxval:
          if self.clipInput:
            if self.verbosity > 0:
              print "Clipped input %s=%.2f to maxval %.2f" % (self.name, input,
                                                              self.maxval)
            input = self.maxval
          else:
            raise Exception('input (%s) greater than range (%s - %s)' %
                            (str(input), str(self.minval), str(self.maxval)))

      if self.periodic:
        centerbin = int((input - self.minval) * self.nInternal / self.range) \
                      + self.padding
      else:
        centerbin = int(((input - self.minval) + self.resolution/2) \
                          / self.resolution ) + self.padding


      # We use the first bit to be set in the encoded output as the bucket index
      minbin = centerbin - self.halfwidth
      return [minbin]