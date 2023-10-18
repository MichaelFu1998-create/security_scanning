def gml_to_geojson(el):
    """Given an lxml Element of a GML geometry, returns a dict in GeoJSON format."""
    if el.get('srsName') not in ('urn:ogc:def:crs:EPSG::4326', None):
        if el.get('srsName') == 'EPSG:4326':
            return _gmlv2_to_geojson(el)
        else:
            raise NotImplementedError("Unrecognized srsName %s" % el.get('srsName'))
    tag = el.tag.replace('{%s}' % NS_GML, '')
    if tag == 'Point':
        coordinates = _reverse_gml_coords(el.findtext('{%s}pos' % NS_GML))[0]
    elif tag == 'LineString':
        coordinates = _reverse_gml_coords(el.findtext('{%s}posList' % NS_GML))
    elif tag == 'Polygon':
        coordinates = []
        for ring in el.xpath('gml:exterior/gml:LinearRing/gml:posList', namespaces=NSMAP) \
                + el.xpath('gml:interior/gml:LinearRing/gml:posList', namespaces=NSMAP):
            coordinates.append(_reverse_gml_coords(ring.text))
    elif tag in ('MultiPoint', 'MultiLineString', 'MultiPolygon'):
        single_type = tag[5:]
        member_tag = single_type[0].lower() + single_type[1:] + 'Member'
        coordinates = [
            gml_to_geojson(member)['coordinates']
            for member in el.xpath('gml:%s/gml:%s' % (member_tag, single_type), namespaces=NSMAP)
        ]
    else:
        raise NotImplementedError

    return {
        'type': tag,
        'coordinates': coordinates
    }