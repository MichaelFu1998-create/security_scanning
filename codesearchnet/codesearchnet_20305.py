def compress_blocking(image, delete_tif=False, folder=None, force=False):
    """Lossless compression. Save image as PNG and TIFF tags to json. Process
    can be reversed with `decompress`.

    Parameters
    ----------
    image : string
        TIF-image which should be compressed lossless.
    delete_tif : bool
        Wheter to delete original images.
    force : bool
        Wheter to compress even if .png already exists.

    Returns
    -------
    string
        Filename of compressed image, or empty string if compress failed.
    """

    debug('compressing {}'.format(image))
    try:
        new_filename, extension = os.path.splitext(image)
        # remove last occurrence of .ome
        new_filename = new_filename.rsplit('.ome', 1)[0]

        # if compressed file should be put in specified folder
        if folder:
            basename = os.path.basename(new_filename)
            new_filename = os.path.join(folder, basename + '.png')
        else:
            new_filename = new_filename + '.png'

        # check if png exists
        if os.path.isfile(new_filename) and not force:
            compressed_images.append(new_filename)
            msg = "Aborting compress, PNG already" \
                  " exists: {}".format(new_filename)
            raise AssertionError(msg)
        if extension != '.tif':
            msg = "Aborting compress, not a TIFF: {}".format(image)
            raise AssertionError(msg)

        # open image, load and close file pointer
        img = Image.open(image)
        fptr = img.fp # keep file pointer, for closing
        img.load() # load img-data before switching mode, also closes fp

        # get tags and save them as json
        tags = img.tag.as_dict()
        with open(new_filename[:-4] + '.json', 'w') as f:
            if img.mode == 'P':
                # keep palette
                tags['palette'] = img.getpalette()
            json.dump(tags, f)

        # check if image is palette-mode
        if img.mode == 'P':
            # switch to luminance to keep data intact
            debug('palette-mode switched to luminance')
            img.mode = 'L'
        if img.mode == 'I;16':
            # https://github.com/python-pillow/Pillow/issues/1099
            img = img.convert(mode='I')

        # compress/save
        debug('saving to {}'.format(new_filename))
        img.save(new_filename)

        fptr.close() # windows bug Pillow
        if delete_tif:
            os.remove(image)

    except (IOError, AssertionError) as e:
        # print error - continue
        print('leicaexperiment {}'.format(e))
        return ''

    return new_filename