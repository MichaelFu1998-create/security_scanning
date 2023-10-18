def topDownCompute(self, encoded):
    """ See the function description in base.py
    """

    # Get/generate the topDown mapping table
    topDownMappingM = self._getTopDownMapping()

    # See which "category" we match the closest.
    category = topDownMappingM.rightVecProd(encoded).argmax()

    # Return that bucket info
    return self.getBucketInfo([category])