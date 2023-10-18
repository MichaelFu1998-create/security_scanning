def nations(timeout=timeout):
    """Return all nations in dict {id0: nation0, id1: nation1}.

    :params year: Year.
    """
    rc = requests.get(messages_url, timeout=timeout)
    rc.encoding = 'utf-8'  # guessing takes huge amount of cpu time
    rc = rc.text
    data = re.findall('"search.nationName.nation([0-9]+)": "(.+)"', rc)
    nations = {}
    for i in data:
        nations[int(i[0])] = i[1]
    return nations