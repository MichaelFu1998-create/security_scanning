def sanitize_filename(filename):
    """preserve the file ending, but replace the name with a random token """
    # TODO: fix broken splitext (it reveals everything of the filename after the first `.` - doh!)
    token = generate_drop_id()
    name, extension = splitext(filename)
    if extension:
        return '%s%s' % (token, extension)
    else:
        return token