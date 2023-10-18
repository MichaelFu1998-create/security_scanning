def _create_index_file(
        root_dir, location, image_files, dirs, force_no_processing=False):
    """
    Create an index file in the given location, supplying known lists of
    present image files and subdirectories.
    @param {String} root_dir - The root directory of the entire crawl. Used to
        ascertain whether the given location is the top level.
    @param {String} location - The current directory of the crawl. The index
        file will be created here.
    @param {[String]} image_files - A list of image file names in the location.
        These will be displayed in the index file's gallery.
    @param {[String]} dirs - The subdirectories of the location directory.
        These will be displayed as links further down the file structure.
    @param {Boolean=False} force_no_processing - If True, do not attempt to
        actually process thumbnails, PIL images or anything. Simply index
        <img> tags with original file src attributes.
    @return {String} The full path (location plus filename) of the newly
        created index file. Intended for usage cleaning up created files.
    """
    # Put together HTML as a list of the lines we'll want to include
    # Issue #2 exists to do this better than HTML in-code
    header_text = \
        'imageMe: ' + location + ' [' + str(len(image_files)) + ' image(s)]'
    html = [
        '<!DOCTYPE html>',
        '<html>',
        '    <head>',
        '        <title>imageMe</title>'
        '        <style>',
        '            html, body {margin: 0;padding: 0;}',
        '            .header {text-align: right;}',
        '            .content {',
        '                padding: 3em;',
        '                padding-left: 4em;',
        '                padding-right: 4em;',
        '            }',
        '            .image {max-width: 100%; border-radius: 0.3em;}',
        '            td {width: ' + str(100.0 / IMAGES_PER_ROW) + '%;}',
        '        </style>',
        '    </head>',
        '    <body>',
        '    <div class="content">',
        '        <h2 class="header">' + header_text + '</h2>'
    ]
    # Populate the present subdirectories - this includes '..' unless we're at
    # the top level
    directories = []
    if root_dir != location:
        directories = ['..']
    directories += dirs
    if len(directories) > 0:
        html.append('<hr>')
    # For each subdirectory, include a link to its index file
    for directory in directories:
        link = directory + '/' + INDEX_FILE_NAME
        html += [
            '    <h3 class="header">',
            '    <a href="' + link + '">' + directory + '</a>',
            '    </h3>'
        ]
    # Populate the image gallery table
    # Counter to cycle down through table rows
    table_row_count = 1
    html += ['<hr>', '<table>']
    # For each image file, potentially create a new <tr> and create a new <td>
    for image_file in image_files:
        if table_row_count == 1:
            html.append('<tr>')
        img_src = _get_thumbnail_src_from_file(
            location, image_file, force_no_processing
        )
        link_target = _get_image_link_target_from_file(
            location, image_file, force_no_processing
        )
        html += [
            '    <td>',
            '    <a href="' + link_target + '">',
            '        <img class="image" src="' + img_src + '">',
            '    </a>',
            '    </td>'
        ]
        if table_row_count == IMAGES_PER_ROW:
            table_row_count = 0
            html.append('</tr>')
        table_row_count += 1
    html += ['</tr>', '</table>']
    html += [
        '    </div>',
        '    </body>',
        '</html>'
    ]
    # Actually create the file, now we've put together the HTML content
    index_file_path = _get_index_file_path(location)
    print('Creating index file %s' % index_file_path)
    index_file = open(index_file_path, 'w')
    index_file.write('\n'.join(html))
    index_file.close()
    # Return the path for cleaning up later
    return index_file_path