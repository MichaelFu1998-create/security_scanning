def get_encodings_from_content(content):
    """
    Code from:
    https://github.com/sigmavirus24/requests-toolbelt/blob/master/requests_toolbelt/utils/deprecated.py
    Return encodings from given content string.
    :param content: string to extract encodings from.
    """
    if isinstance(content, bytes):
        find_charset = re.compile(
            br'<meta.*?charset=["\']*([a-z0-9\-_]+?) *?["\'>]', flags=re.I
        ).findall

        find_xml = re.compile(
            br'^<\?xml.*?encoding=["\']*([a-z0-9\-_]+?) *?["\'>]'
        ).findall
        return [encoding.decode('utf-8') for encoding in
                find_charset(content) + find_xml(content)]
    else:
        find_charset = re.compile(
            r'<meta.*?charset=["\']*([a-z0-9\-_]+?) *?["\'>]', flags=re.I
        ).findall

        find_xml = re.compile(
            r'^<\?xml.*?encoding=["\']*([a-z0-9\-_]+?) *?["\'>]'
        ).findall
        return find_charset(content) + find_xml(content)