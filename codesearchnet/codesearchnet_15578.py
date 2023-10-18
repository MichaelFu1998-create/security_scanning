def NextPage(gh):
    """
    Checks if a GitHub call returned multiple pages of data.

    :param gh: GitHub() instance
    :rtype: int
    :return: number of next page or 0 if no next page
    """
    header = dict(gh.getheaders())
    if 'Link' in header:
        parts = header['Link'].split(',')
        for part in parts:
            subparts = part.split(';')
            sub = subparts[1].split('=')
            if sub[0].strip() == 'rel':
                if sub[1] == '"next"':
                    page = int(
                        re.match(
                            r'.*page=(\d+).*', subparts[0],
                            re.IGNORECASE | re.DOTALL | re.UNICODE
                        ).groups()[0]
                    )
                    return page
    return 0