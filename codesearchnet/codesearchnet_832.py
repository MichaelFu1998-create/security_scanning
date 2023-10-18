def getRegionsByType(self, regionClass):
    """
    Gets all region instances of a given class
    (for example, nupic.regions.sp_region.SPRegion).
    """
    regions = []

    for region in self.regions.values():
      if type(region.getSelf()) is regionClass:
        regions.append(region)

    return regions