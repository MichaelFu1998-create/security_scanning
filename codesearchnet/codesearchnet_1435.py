def topDownCompute(self, encoded):
    """[ScalarEncoder class method override]"""

    #Decode to delta scalar
    if self._prevAbsolute==None or self._prevDelta==None:
      return [EncoderResult(value=0, scalar=0,
                             encoding=numpy.zeros(self.n))]
    ret = self._adaptiveScalarEnc.topDownCompute(encoded)
    if self._prevAbsolute != None:
      ret = [EncoderResult(value=ret[0].value+self._prevAbsolute,
                          scalar=ret[0].scalar+self._prevAbsolute,
                          encoding=ret[0].encoding)]
#      ret[0].value+=self._prevAbsolute
#      ret[0].scalar+=self._prevAbsolute
    return ret