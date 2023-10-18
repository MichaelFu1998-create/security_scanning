def getBucketInfo(self, buckets):
    """
    See the function description in base.py
    """

    scaledResult = self.encoder.getBucketInfo(buckets)[0]
    scaledValue = scaledResult.value
    value = math.pow(10, scaledValue)

    return [EncoderResult(value=value, scalar=value,
                         encoding = scaledResult.encoding)]