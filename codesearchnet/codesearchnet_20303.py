def stitch_macro(path, output_folder=None):
    """Create fiji-macros for stitching all channels and z-stacks for a well.

    Parameters
    ----------
    path : string
        Well path.
    output_folder : string
        Folder to store images. If not given well path is used.

    Returns
    -------
    output_files, macros : tuple
        Tuple with filenames and macros for stitched well.
    """
    output_folder = output_folder or path
    debug('stitching ' + path + ' to ' + output_folder)

    fields = glob(_pattern(path, _field))

    # assume we have rectangle of fields
    xs = [attribute(field, 'X') for field in fields]
    ys = [attribute(field, 'Y') for field in fields]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    fields_column = len(set(xs))
    fields_row = len(set(ys))

    # assume all fields are the same
    # and get properties from images in first field
    images = glob(_pattern(fields[0], _image))

    # assume attributes are the same on all images
    attr = attributes(images[0])

    # find all channels and z-stacks
    channels = []
    z_stacks = []
    for image in images:
        channel = attribute_as_str(image, 'C')
        if channel not in channels:
            channels.append(channel)

        z = attribute_as_str(image, 'Z')
        if z not in z_stacks:
            z_stacks.append(z)

    debug('channels ' + str(channels))
    debug('z-stacks ' + str(z_stacks))

    # create macro
    _, extension = os.path.splitext(images[-1])
    if extension == '.tif':
        # assume .ome.tif
        extension = '.ome.tif'
    macros = []
    output_files = []
    for Z in z_stacks:
        for C in channels:
            filenames = os.path.join(

                    _field + '--X{xx}--Y{yy}',
                    _image + '--L' + attr.L +
                    '--S' + attr.S +
                    '--U' + attr.U +
                    '--V' + attr.V +
                    '--J' + attr.J +
                    '--E' + attr.E +
                    '--O' + attr.O +
                    '--X{xx}--Y{yy}' +
                    '--T' + attr.T +
                    '--Z' + Z +
                    '--C' + C +
                    extension)
            debug('filenames ' + filenames)

            cur_attr = attributes(filenames)._asdict()
            f = 'stitched--U{U}--V{V}--C{C}--Z{Z}.png'.format(**cur_attr)

            output = os.path.join(output_folder, f)
            debug('output ' + output)
            output_files.append(output)
            if os.path.isfile(output):
                # file already exists
                print('leicaexperiment stitched file already'
                      ' exists {}'.format(output))
                continue
            macros.append(fijibin.macro.stitch(path, filenames,
                                  fields_column, fields_row,
                                  output_filename=output,
                                  x_start=x_min, y_start=y_min))

    return (output_files, macros)