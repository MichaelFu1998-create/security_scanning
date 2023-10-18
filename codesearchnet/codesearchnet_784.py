def _categoryToLabelList(self, category):
    """
    Converts a category number into a list of labels
    """
    if category is None:
      return []

    labelList = []
    labelNum = 0
    while category > 0:
      if category % 2 == 1:
        labelList.append(self.saved_categories[labelNum])
      labelNum += 1
      category = category >> 1
    return labelList