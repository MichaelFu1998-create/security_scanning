def from_shapely(geometry, label=None):
        """
        Create a MultiPolygon from a Shapely MultiPolygon, a Shapely Polygon or a Shapely GeometryCollection.

        This also creates all necessary Polygons contained by this MultiPolygon.

        Parameters
        ----------
        geometry : shapely.geometry.MultiPolygon or shapely.geometry.Polygon\
                   or shapely.geometry.collection.GeometryCollection
            The object to convert to a MultiPolygon.

        label : None or str, optional
            A label assigned to all Polygons within the MultiPolygon.

        Returns
        -------
        imgaug.MultiPolygon
            The derived MultiPolygon.

        """
        # load shapely lazily, which makes the dependency more optional
        import shapely.geometry

        if isinstance(geometry, shapely.geometry.MultiPolygon):
            return MultiPolygon([Polygon.from_shapely(poly, label=label) for poly in geometry.geoms])
        elif isinstance(geometry, shapely.geometry.Polygon):
            return MultiPolygon([Polygon.from_shapely(geometry, label=label)])
        elif isinstance(geometry, shapely.geometry.collection.GeometryCollection):
            ia.do_assert(all([isinstance(poly, shapely.geometry.Polygon) for poly in geometry.geoms]))
            return MultiPolygon([Polygon.from_shapely(poly, label=label) for poly in geometry.geoms])
        else:
            raise Exception("Unknown datatype '%s'. Expected shapely.geometry.Polygon or "
                            "shapely.geometry.MultiPolygon or "
                            "shapely.geometry.collections.GeometryCollection." % (type(geometry),))