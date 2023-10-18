def decompress(images, delete_png=False, delete_json=False, folder=None):
    """Reverse compression from tif to png and save them in original format
    (ome.tif). TIFF-tags are gotten from json-files named the same as given
    images.


    Parameters
    ----------
    images : list of filenames
        Image to decompress.
    delete_png : bool
        Wheter to delete PNG images.
    delete_json : bool
        Wheter to delete TIFF-tags stored in json files on compress.

    Returns
    -------
    list of filenames
        List of decompressed files.
    """
    if type(images) == str:
        # only one image
        return decompress([images])

    filenames = copy(images) # as images property will change when looping

    decompressed_images = []
    for orig_filename in filenames:
        debug('decompressing {}'.format(orig_filename))
        try:
            filename, extension = os.path.splitext(orig_filename)

            # if decompressed file should be put in specified folder
            if folder:
                basename = os.path.basename(filename)
                new_filename = os.path.join(folder, basename + '.ome.tif')
            else:
                new_filename = filename + '.ome.tif'

            # check if tif exists
            if os.path.isfile(new_filename):
                decompressed_images.append(new_filename)
                msg = "Aborting decompress, TIFF already exists:" \
                      " {}".format(orig_filename)
                raise AssertionError(msg)
            if extension != '.png':
                msg = "Aborting decompress, not a " \
                      "PNG: {}".format(orig_filename)
                raise AssertionError(msg)

            # open image, load and close file pointer
            img = Image.open(orig_filename)
            img.load() # load img-data before switching mode, also closes fp

            # get tags from json
            info = {}
            with open(filename + '.json', 'r') as f:
                tags = json.load(f)
                # convert dictionary to original types (lost in json conversion)
                for tag,val in tags.items():
                    if tag == 'palette':
                        # hack hack
                        continue
                    if type(val) == list:
                        val = tuple(val)
                    if type(val[0]) == list:
                        # list of list
                        val = tuple(tuple(x) for x in val)
                    info[int(tag)] = val

            # check for color map
            if 'palette' in tags:
                img.putpalette(tags['palette'])

            # save as tif
            debug('saving to {}'.format(new_filename))
            img.save(new_filename, tiffinfo=info)
            decompressed_images.append(new_filename)

            if delete_png:
                os.remove(orig_filename)
            if delete_json:
                os.remove(filename + '.json')

        except (IOError, AssertionError) as e:
            # print error - continue
            print('leicaexperiment {}'.format(e))

    return decompressed_images