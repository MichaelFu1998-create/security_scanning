def _getRegions(self):
    """Get the collection of regions in a network

    This is a tricky one. The collection of regions returned from
    from the internal network is a collection of internal regions.
    The desired collection is a collelcion of net.Region objects
    that also points to this network (net.network) and not to
    the internal network. To achieve that a CollectionWrapper
    class is used with a custom makeRegion() function (see bellow)
    as a value wrapper. The CollectionWrapper class wraps each value in the
    original collection with the result of the valueWrapper.
    """

    def makeRegion(name, r):
      """Wrap a engine region with a nupic.engine_internal.Region

      Also passes the containing nupic.engine_internal.Network network in _network. This
      function is passed a value wrapper to the CollectionWrapper
      """
      r = Region(r, self)
      #r._network = self
      return r

    regions = CollectionWrapper(engine_internal.Network.getRegions(self), makeRegion)
    return regions