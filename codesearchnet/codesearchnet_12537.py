def tilemap(self, query, styles={}, bbox=[-180,-90,180,90], zoom=16, 
                      api_key=os.environ.get('MAPBOX_API_KEY', None), 
                      image=None, image_bounds=None,
                      index="vector-user-provided", name="GBDX_Task_Output", **kwargs):
        """
          Renders a mapbox gl map from a vector service query
        """
        try:
            from IPython.display import display
        except:
            print("IPython is required to produce maps.")
            return

        assert api_key is not None, "No Mapbox API Key found. You can either pass in a token or set the MAPBOX_API_KEY environment variable."

        wkt = box(*bbox).wkt
        features = self.query(wkt, query, index=index)

        union = cascaded_union([shape(f['geometry']) for f in features])
        lon, lat = union.centroid.coords[0]
        url = 'https://vector.geobigdata.io/insight-vector/api/mvt/{z}/{x}/{y}?';
        url += 'q={}&index={}'.format(query, index);

        if styles is not None and not isinstance(styles, list):
            styles = [styles]

        map_id = "map_{}".format(str(int(time.time())))
        map_data = VectorTileLayer(url, source_name=name, styles=styles, **kwargs)
        image_layer = self._build_image_layer(image, image_bounds)

        template = BaseTemplate(map_id, **{
            "lat": lat,
            "lon": lon,
            "zoom": zoom,
            "datasource": json.dumps(map_data.datasource),
            "layers": json.dumps(map_data.layers),
            "image_layer": image_layer,
            "mbkey": api_key,
            "token": self.gbdx_connection.access_token
        })
        
        template.inject()