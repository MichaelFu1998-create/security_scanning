def map(self, features=None, query=None, styles=None,
                  bbox=[-180,-90,180,90], zoom=10, center=None, 
                  image=None, image_bounds=None, cmap='viridis',
                  api_key=os.environ.get('MAPBOX_API_KEY', None), **kwargs):
        """
          Renders a mapbox gl map from a vector service query or a list of geojson features

          Args:
            features (list): a list of geojson features
            query (str): a VectorServices query 
            styles (list): a list of VectorStyles to apply to the features  
            bbox (list): a bounding box to query for features ([minx, miny, maxx, maxy])
            zoom (int): the initial zoom level of the map
            center (list): a list of [lat, lon] used to center the map
            api_key (str): a valid Mapbox API key
            image (dict): a CatalogImage or a ndarray
            image_bounds (list): a list of bounds for image positioning 
            Use outside of GBDX Notebooks requires a MapBox API key, sign up for free at https://www.mapbox.com/pricing/
            Pass the key using the `api_key` keyword or set an environmental variable called `MAPBOX API KEY`
            cmap (str): MatPlotLib colormap to use for rendering single band images (default: viridis)
        """
        try:
            from IPython.display import display
        except:
            print("IPython is required to produce maps.")
            return

        assert api_key is not None, "No Mapbox API Key found. You can either pass in a key or set the MAPBOX_API_KEY environment variable. Use outside of GBDX Notebooks requires a MapBox API key, sign up for free at https://www.mapbox.com/pricing/"
        if features is None and query is not None:
            wkt = box(*bbox).wkt
            features = self.query(wkt, query, index=None)
        elif features is None and query is None and image is None:
            print('Must provide either a list of features or a query or an image')
            return

        if styles is not None and not isinstance(styles, list):
            styles = [styles]

        geojson = {"type":"FeatureCollection", "features": features}

        if center is None and features is not None:
            union = cascaded_union([shape(f['geometry']) for f in features])
            lon, lat = union.centroid.coords[0]
        elif center is None and image is not None:
            try:
                lon, lat = shape(image).centroid.coords[0]
            except:
                lon, lat = box(*image_bounds).centroid.coords[0]
        else:
            lat, lon = center

        map_id = "map_{}".format(str(int(time.time())))
        map_data = VectorGeojsonLayer(geojson, styles=styles, **kwargs)
        image_layer = self._build_image_layer(image, image_bounds, cmap)

        template = BaseTemplate(map_id, **{
            "lat": lat, 
            "lon": lon, 
            "zoom": zoom,
            "datasource": json.dumps(map_data.datasource),
            "layers": json.dumps(map_data.layers),
            "image_layer": image_layer,
            "mbkey": api_key,
            "token": 'dummy'
        })
        template.inject()