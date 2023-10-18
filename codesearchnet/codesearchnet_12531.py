def create(self,vectors):
        """ Create a vectors in the vector service.

        Args:
            vectors: A single geojson vector or a list of geojson vectors. Item_type and ingest_source are required.

        Returns:
            (list): IDs of the vectors created

        Example:
            >>> vectors.create(
            ...     {
            ...         "type": "Feature",
            ...         "geometry": {
            ...             "type": "Point",
            ...             "coordinates": [1.0,1.0]
            ...         },
            ...         "properties": {
            ...             "text" : "item text",
            ...             "name" : "item name",
            ...             "item_type" : "type",
            ...             "ingest_source" : "source",
            ...             "attributes" : {
            ...                 "latitude" : 1,
            ...                 "institute_founded" : "2015-07-17",
            ...                 "mascot" : "moth"
            ...             }
            ...         }
            ...     }
            ... )

        """
        if type(vectors) is dict:
            vectors = [vectors]

        # validate they all have item_type and ingest_source in properties
        for vector in vectors:
            if not 'properties' in list(vector.keys()):
                raise Exception('Vector does not contain "properties" field.')

            if not 'item_type' in list(vector['properties'].keys()):
                raise Exception('Vector does not contain "item_type".')

            if not 'ingest_source' in list(vector['properties'].keys()):
                raise Exception('Vector does not contain "ingest_source".')

        r = self.gbdx_connection.post(self.create_url, data=json.dumps(vectors))
        r.raise_for_status()
        return r.json()