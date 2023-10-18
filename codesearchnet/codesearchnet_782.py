def _labelToCategoryNumber(self, label):
    """
    Since the KNN Classifier stores categories as numbers, we must store each
    label as a number. This method converts from a label to a unique number.
    Each label is assigned a unique bit so multiple labels may be assigned to
    a single record.
    """
    if label not in self.saved_categories:
      self.saved_categories.append(label)
    return pow(2, self.saved_categories.index(label))