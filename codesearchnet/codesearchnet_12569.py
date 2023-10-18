def get_data_location(self, catalog_id):
        """
        Find and return the S3 data location given a catalog_id.

        Args:
            catalog_id: The catalog ID

        Returns:
            A string containing the s3 location of the data associated with a catalog ID.  Returns
            None if the catalog ID is not found, or if there is no data yet associated with it.
        """

        try:
            record = self.get(catalog_id)
        except:
            return None

        # Handle Landsat8
        if 'Landsat8' in record['type'] and 'LandsatAcquisition' in record['type']:
            bucket = record['properties']['bucketName']
            prefix = record['properties']['bucketPrefix']
            return 's3://' + bucket + '/' + prefix

        # Handle DG Acquisition
        if 'DigitalGlobeAcquisition' in record['type']:
            o = Ordering()
            res = o.location([catalog_id])
            return res['acquisitions'][0]['location']

        return None