def write_var_data(fd, data):
    """Write variable data to file"""
    # write array data elements (size info)
    fd.write(struct.pack('b3xI', etypes['miMATRIX']['n'], len(data)))

    # write the data
    fd.write(data)