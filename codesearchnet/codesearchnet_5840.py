def check_url(url):
    """
    Function that verifies that the string passed is a valid url.

    Original regex author Diego Perini (http://www.iport.it)
    regex ported to Python by adamrofer (https://github.com/adamrofer)
    Used under MIT license.

    :param url:
    :return: Nothing
    """
    URL_REGEX = re.compile(
    u"^"
    u"(?:(?:https?|ftp)://)"
    u"(?:\S+(?::\S*)?@)?"
    u"(?:"
    u"(?!(?:10|127)(?:\.\d{1,3}){3})"
    u"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    u"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    u"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    u"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    u"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    u"|"
    u"(?:(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)"
    u"(?:\.(?:[a-z\u00a1-\uffff0-9]-?)*[a-z\u00a1-\uffff0-9]+)*"
    u"(?:\.(?:[a-z\u00a1-\uffff]{2,}))"
    u")"
    u"(?::\d{2,5})?"
    u"(?:/\S*)?"
    u"$"
    , re.UNICODE)
    if not re.match(URL_REGEX, url):
        raise ValueError('String passed is not a valid url')
    return