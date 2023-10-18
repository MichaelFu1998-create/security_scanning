def geojson_to_gml(gj, set_srs=True):
    """Given a dict deserialized from a GeoJSON object, returns an lxml Element
    of the corresponding GML geometry."""
    tag = G(gj['type'])
    if set_srs:
        tag.set('srsName', 'urn:ogc:def:crs:EPSG::4326')

    if gj['type'] == 'Point':
        tag.append(G.pos(_reverse_geojson_coords(gj['coordinates'])))
    elif gj['type'] == 'LineString':
        tag.append(G.posList(' '.join(_reverse_geojson_coords(ll) for ll in gj['coordinates'])))
    elif gj['type'] == 'Polygon':
        rings = [
            G.LinearRing(
                G.posList(' '.join(_reverse_geojson_coords(ll) for ll in ring))
            ) for ring in gj['coordinates']
        ]
        tag.append(G.exterior(rings.pop(0)))
        for ring in rings:
            tag.append(G.interior(ring))
    elif gj['type'] in ('MultiPoint', 'MultiLineString', 'MultiPolygon'):
        single_type = gj['type'][5:]
        member_tag = single_type[0].lower() + single_type[1:] + 'Member'
        for coord in gj['coordinates']:
            tag.append(
                G(member_tag, geojson_to_gml({'type': single_type, 'coordinates': coord}, set_srs=False))
            )
    else:
        raise NotImplementedError

    return tag