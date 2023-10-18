def describe_images(self, idaho_image_results):
        """Describe the result set of a catalog search for IDAHO images.

        Args:
            idaho_image_results (dict): Result set of catalog search.
        Returns:
            results (json): The full catalog-search response for IDAHO images
                            corresponding to the given catID.
        """

        results = idaho_image_results['results']

        # filter only idaho images:
        results = [r for r in results if 'IDAHOImage' in r['type']]
        self.logger.debug('Describing %s IDAHO images.' % len(results))

        # figure out which catids are represented in this set of images
        catids = set([r['properties']['catalogID'] for r in results])

        description = {}

        for catid in catids:
            # images associated with a single catid
            description[catid] = {}
            description[catid]['parts'] = {}
            images = [r for r in results if r['properties']['catalogID'] == catid]
            for image in images:
                description[catid]['sensorPlatformName'] = image['properties']['sensorPlatformName']
                part = int(image['properties']['vendorDatasetIdentifier'].split(':')[1][-3:])
                color = image['properties']['colorInterpretation']
                bucket = image['properties']['tileBucketName']
                identifier = image['identifier']
                boundstr = image['properties']['footprintWkt']

                try:
                    description[catid]['parts'][part]
                except:
                    description[catid]['parts'][part] = {}

                description[catid]['parts'][part][color] = {}
                description[catid]['parts'][part][color]['id'] = identifier
                description[catid]['parts'][part][color]['bucket'] = bucket
                description[catid]['parts'][part][color]['boundstr'] = boundstr

        return description