def iso_path_slugify(path, path_table, is_dir=False, strict=True):
    """Slugify a path, maintaining a map with the previously slugified paths.

    The path table is used to prevent slugified names from collisioning,
    using the `iso_name_increment` function to deduplicate slugs.

    Example:
        >>> path_table = {'/': '/'}
        >>> iso_path_slugify('/ébc.txt', path_table)
        '/_BC.TXT'
        >>> iso_path_slugify('/àbc.txt', path_table)
        '/_BC2.TXT'
    """
    # Split the path to extract the parent and basename
    parent, base = split(path)

    # Get the parent in slugified form
    slug_parent = path_table[parent]

    # Slugify the base name
    if is_dir:
        slug_base = iso_name_slugify(base)[:8]
    else:
        name, ext = base.rsplit('.', 1) if '.' in base else (base, '')
        slug_base = '.'.join([iso_name_slugify(name)[:8], ext])
    if strict:
        slug_base = slug_base.upper()

    # Deduplicate slug if needed and update path_table
    slugs = set(path_table.values())
    path_table[path] = slug = join(slug_parent, slug_base)
    while slug in slugs:
        slug_base = iso_name_increment(slug_base, is_dir)
        path_table[path] = slug = join(slug_parent, slug_base)

    # Return the unique slug
    return slug