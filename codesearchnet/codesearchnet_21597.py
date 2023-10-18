def _gmlv2_to_geojson(el):
    """Translates a deprecated GML 2.0 geometry to GeoJSON"""
    tag = el.tag.replace('{%s}' % NS_GML, '')
    if tag == 'Point':
        coordinates = [float(c) for c in el.findtext('{%s}coordinates' % NS_GML).split(',')]
    elif tag == 'LineString':
        coordinates = [
            [float(x) for x in pair.split(',')]
            for pair in el.findtext('{%s}coordinates' % NS_GML).split(' ')
        ]
    elif tag == 'Polygon':
        coordinates = []
        for ring in el.xpath('gml:outerBoundaryIs/gml:LinearRing/gml:coordinates', namespaces=NSMAP) \
                + el.xpath('gml:innerBoundaryIs/gml:LinearRing/gml:coordinates', namespaces=NSMAP):
            coordinates.append([
                [float(x) for x in pair.split(',')]
                for pair in ring.text.split(' ')
            ])
    elif tag in ('MultiPoint', 'MultiLineString', 'MultiPolygon', 'MultiCurve'):
        if tag == 'MultiCurve':
            single_type = 'LineString'
            member_tag = 'curveMember'
        else:
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