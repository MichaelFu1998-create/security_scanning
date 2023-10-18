def getBucketInfo(self, buckets):
    """ See the function description in base.py """

    # Get/generate the topDown mapping table
    #NOTE: although variable topDownMappingM is unused, some (bad-style) actions
    #are executed during _getTopDownMapping() so this line must stay here
    topDownMappingM = self._getTopDownMapping()

    # The "category" is simply the bucket index
    category = buckets[0]
    encoding = self._topDownMappingM.getRow(category)

    # Which input value does this correspond to?
    if self.periodic:
      inputVal = (self.minval + (self.resolution / 2.0) +
                  (category * self.resolution))
    else:
      inputVal = self.minval + (category * self.resolution)

    return [EncoderResult(value=inputVal, scalar=inputVal, encoding=encoding)]