def add_geo(self, geo_location):
        """
        Saves a <geo-location> Element, to be incoporated into the Open511
        geometry field.
        """
        if not geo_location.xpath('latitude') and geo_location.xpath('longitude'):
            raise Exception("Invalid geo-location %s" % etree.tostring(geo_location))
        if _xpath_or_none(geo_location, 'horizontal-datum/text()') not in ('wgs84', None):
            logger.warning("Unsupported horizontal-datum in %s" % etree.tostring(geo_location))
            return
        point = (
            float(_xpath_or_none(geo_location, 'longitude/text()')) / 1000000,
            float(_xpath_or_none(geo_location, 'latitude/text()')) / 1000000
        )
        self.points.add(point)