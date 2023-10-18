def players(timeout=timeout):
    """Return all players in dict {id: c, f, l, n, r}.
    id, rank, nationality(?), first name, last name.
    """
    rc = requests.get('{0}{1}.json'.format(card_info_url, 'players'), timeout=timeout).json()
    players = {}
    for i in rc['Players'] + rc['LegendsPlayers']:
        players[i['id']] = {'id': i['id'],
                            'firstname': i['f'],
                            'lastname': i['l'],
                            'surname': i.get('c'),
                            'rating': i['r']}
    return players