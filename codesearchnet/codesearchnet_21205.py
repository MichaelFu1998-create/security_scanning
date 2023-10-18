def filename(file_name, start_on=None, ignore=(), use_short=True, **queries):
    '''Returns a blox template from a valid file path'''
    with open(file_name) as template_file:
        return file(template_file, start_on=start_on, ignore=ignore, use_short=use_short, **queries)