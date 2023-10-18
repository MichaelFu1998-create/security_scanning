def remapCategories(self, mapping):
    """Change the category indices.

    Used by the Network Builder to keep the category indices in sync with the
    ImageSensor categoryInfo when the user renames or removes categories.

    :param mapping: List of new category indices. For example, mapping=[2,0,1]
        would change all vectors of category 0 to be category 2, category 1 to
        0, and category 2 to 1
    """
    categoryArray = numpy.array(self._categoryList)
    newCategoryArray = numpy.zeros(categoryArray.shape[0])
    newCategoryArray.fill(-1)
    for i in xrange(len(mapping)):
      newCategoryArray[categoryArray==i] = mapping[i]
    self._categoryList = list(newCategoryArray)