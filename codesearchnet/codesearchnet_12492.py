def get_images_by_catid_and_aoi(self, catid, aoi_wkt):
        """ Retrieves the IDAHO image records associated with a given catid.
        Args:
            catid (str): The source catalog ID from the platform catalog.
            aoi_wkt (str): The well known text of the area of interest.
        Returns:
            results (json): The full catalog-search response for IDAHO images
                            within the catID.
        """

        self.logger.debug('Retrieving IDAHO metadata')

        # use the footprint to get the IDAHO id
        url = '%s/search' % self.base_url

        body = {"filters": ["catalogID = '%s'" % catid],
                "types": ["IDAHOImage"],
                "searchAreaWkt": aoi_wkt}

        r = self.gbdx_connection.post(url, data=json.dumps(body))

        r.raise_for_status()
        if r.status_code == 200:
            results = r.json()
            numresults = len(results['results'])
            self.logger.debug('%s IDAHO images found associated with catid %s'
                              % (numresults, catid))

            return results