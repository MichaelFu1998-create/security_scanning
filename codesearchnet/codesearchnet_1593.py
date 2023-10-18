def topDownCompute(self, encoded):
    """
    See the function description in base.py
    """

    scaledResult = self.encoder.topDownCompute(encoded)[0]
    scaledValue = scaledResult.value
    value = math.pow(10, scaledValue)

    return EncoderResult(value=value, scalar=value,
                         encoding = scaledResult.encoding)