def create_from_wkt(self, wkt, item_type, ingest_source, **attributes):
        '''
        Create a single vector in the vector service

        Args:
            wkt (str): wkt representation of the geometry
            item_type (str): item_type of the vector
            ingest_source (str): source of the vector
            attributes: a set of key-value pairs of attributes

        Returns:
            id (str): string identifier of the vector created
        '''
        # verify the "depth" of the attributes is single layer

        geojson = load_wkt(wkt).__geo_interface__
        vector = {
            'type': "Feature",
            'geometry': geojson,
            'properties': {
                'item_type': item_type,
                'ingest_source': ingest_source,
                'attributes': attributes
            }
        }

        return self.create(vector)[0]