def write_compressed_var_array(fd, array, name):
    """Write compressed variable data to file"""
    bd = BytesIO()

    write_var_array(bd, array, name)

    data = zlib.compress(bd.getvalue())
    bd.close()

    # write array data elements (size info)
    fd.write(struct.pack('b3xI', etypes['miCOMPRESSED']['n'], len(data)))

    # write the compressed data
    fd.write(data)