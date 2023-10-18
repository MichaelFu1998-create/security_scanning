def get_images_by_catid(self, catid):
        """ Retrieves the IDAHO image records associated with a given catid.
        Args:
            catid (str): The source catalog ID from the platform catalog.
        Returns:
            results (json): The full catalog-search response for IDAHO images
                            within the catID.
        """

        self.logger.debug('Retrieving IDAHO metadata')

        # get the footprint of the catid's strip
        footprint = self.catalog.get_strip_footprint_wkt(catid)

        # try to convert from multipolygon to polygon:
        try:
            footprint = from_wkt(footprint).geoms[0].wkt
        except:
            pass

        if not footprint:
            self.logger.debug("""Cannot get IDAHO metadata for strip %s,
                                 footprint not found""" % catid)
            return None

        return self.get_images_by_catid_and_aoi(catid=catid,
                                                aoi_wkt=footprint)