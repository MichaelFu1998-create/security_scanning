def combine_files(*args):
    """returns a string of all the strings in *args combined together,
    with two line breaks between them"""
    file_contents = []
    for filename in args:
        with codecs.open(filename, mode='r', encoding='utf8') as f:
            file_contents.append(f.read())
    return "\n\n".join(file_contents)