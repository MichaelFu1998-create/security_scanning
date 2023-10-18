def geom_to_xml_element(geom):
    """Transform a GEOS or OGR geometry object into an lxml Element
    for the GML geometry."""
    if geom.srs.srid != 4326:
        raise NotImplementedError("Only WGS 84 lat/long geometries (SRID 4326) are supported.")
    # GeoJSON output is far more standard than GML, so go through that
    return geojson_to_gml(json.loads(geom.geojson))