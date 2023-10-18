def getBucketInfo(self, buckets):
    """ See the function description in base.py
    """

    # For the category encoder, the bucket index is the category index
    bucketInfo = self.encoder.getBucketInfo(buckets)[0]

    categoryIndex = int(round(bucketInfo.value))
    category = self.indexToCategory[categoryIndex]

    return [EncoderResult(value=category, scalar=categoryIndex,
                         encoding=bucketInfo.encoding)]