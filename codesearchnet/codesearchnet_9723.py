def write_shapefile(data, shapefile_path):
    from numpy import int64
    """
    :param data: list of dicts where dictionary contains the keys lons and lats
    :param shapefile_path: path where shapefile is saved
    :return:
    """

    w = shp.Writer(shp.POLYLINE)  # shapeType=3)

    fields = []
    encode_strings = []

    # This makes sure every geom has all the attributes
    w.autoBalance = 1
    # Create all attribute fields except for lats and lons. In addition the field names are saved for the
    # datastoring phase. Encode_strings stores .encode methods as strings for all fields that are strings
    if not fields:
        for key, value in data[0].items():
            if key != u'lats' and key != u'lons':
                fields.append(key)

                if type(value) == float:
                    w.field(key.encode('ascii'), fieldType='N', size=11, decimal=3)
                    print("float", type(value))
                elif type(value) == int or type(value) == int64:
                    print("int", type(value))

                    # encode_strings.append(".encode('ascii')")
                    w.field(key.encode('ascii'), fieldType='N', size=6, decimal=0)
                else:
                    print("other type", type(value))

                    w.field(key.encode('ascii'))

    for dict_item in data:
        line = []
        lineparts = []
        records = []
        records_string = ''
        for lat, lon in zip(dict_item[u'lats'], dict_item[u'lons']):
            line.append([float(lon), float(lat)])
        lineparts.append(line)
        w.line(parts=lineparts)

        # The shapefile records command is built up as strings to allow a differing number of columns
        for field in fields:
            if records_string:
                records_string += ", dict_item['" + field + "']"
            else:
                records_string += "dict_item['" + field + "']"
        method_string = "w.record(" + records_string + ")"

        # w.record(dict_item['name'], dict_item['agency'], dict_item['agency_name'], dict_item['type'], dict_item['lons'])
        print(method_string)
        eval(method_string)
    w.save(shapefile_path)