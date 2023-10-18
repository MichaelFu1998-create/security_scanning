def populateCategoriesOut(self, categories, output):
    """
    Populate the output array with the category indices.
    
    .. note:: Non-categories are represented with ``-1``.

    :param categories: (list) of category strings
    :param output: (list) category output, will be overwritten
    """
    if categories[0] is None:
      # The record has no entry in category field.
      output[:] = -1
    else:
      # Populate category output array by looping over the smaller of the
      # output array (size specified by numCategories) and the record's number
      # of categories.
      for i, cat in enumerate(categories[:len(output)]):
        output[i] = cat
      output[len(categories):] = -1