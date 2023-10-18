def getDistances(self, inputPattern):
    """Return the distances between the input pattern and all other
    stored patterns.

    :param inputPattern: pattern to check distance with

    :returns: (distances, categories) numpy arrays of the same length.
        - overlaps: an integer overlap amount for each category
        - categories: category index for each element of distances
    """
    dist = self._getDistances(inputPattern)
    return (dist, self._categoryList)