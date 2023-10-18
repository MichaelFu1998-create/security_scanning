def topDownCompute(self, encoded):
    """ See the function description in base.py
    """

    encoderResult = self.encoder.topDownCompute(encoded)[0]
    value = encoderResult.value
    categoryIndex = int(round(value))
    category = self.indexToCategory[categoryIndex]

    return EncoderResult(value=category, scalar=categoryIndex,
                         encoding=encoderResult.encoding)