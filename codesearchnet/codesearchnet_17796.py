def iso_name_increment(name, is_dir=False, max_length=8):
    """Increment an ISO name to avoid name collision.

    Example:
        >>> iso_name_increment('foo.txt')
        'foo1.txt'
        >>> iso_name_increment('bar10')
        'bar11'
        >>> iso_name_increment('bar99', max_length=5)
        'ba100'
    """
    # Split the extension if needed
    if not is_dir and '.' in name:
        name, ext = name.rsplit('.')
        ext = '.{}'.format(ext)
    else:
        ext = ''

    # Find the position of the last letter
    for position, char in reversed(list(enumerate(name))):
        if char not in string.digits:
            break

    # Extract the numbers and the text from the name
    base, tag = name[:position+1], name[position+1:]
    tag = str(int(tag or 0) + 1)

    # Crop the text if the numbers are too long
    if len(tag) + len(base) > max_length:
        base = base[:max_length - len(tag)]

    # Return the name with the extension
    return ''.join([base, tag, ext])