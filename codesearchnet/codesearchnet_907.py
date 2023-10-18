def topDownCompute(self, encoded):
    """ See the function description in base.py
    """

    if self.ncategories==0:
      return 0

    topDownMappingM = self._getTopDownMapping()

    categoryIndex = topDownMappingM.rightVecProd(encoded).argmax()
    category = self.categories[categoryIndex]
    encoding = topDownMappingM.getRow(categoryIndex)

    return EncoderResult(value=category, scalar=categoryIndex, encoding=encoding)