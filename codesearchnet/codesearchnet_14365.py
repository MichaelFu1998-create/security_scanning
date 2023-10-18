def _code_search(query, github_user=None):
    """Performs a Github API code search

    Args:
        query (str): The query sent to Github's code search
        github_user (str, optional): The Github user being searched in the query string

    Returns:
        dict: A dictionary of repository information keyed on the git SSH url

    Raises:
        `InvalidGithubUserError`: When ``github_user`` is invalid
    """
    github_client = temple.utils.GithubClient()
    headers = {'Accept': 'application/vnd.github.v3.text-match+json'}

    resp = github_client.get('/search/code',
                             params={'q': query, 'per_page': 100},
                             headers=headers)

    if resp.status_code == requests.codes.unprocessable_entity and github_user:
        raise temple.exceptions.InvalidGithubUserError(
            'Invalid Github user or org - "{}"'.format(github_user))
    resp.raise_for_status()

    resp_data = resp.json()

    repositories = collections.defaultdict(dict)
    while True:
        repositories.update({
            'git@github.com:{}.git'.format(repo['repository']['full_name']): repo['repository']
            for repo in resp_data['items']
        })

        next_url = _parse_link_header(resp.headers).get('next')
        if next_url:
            resp = requests.get(next_url, headers=headers)
            resp.raise_for_status()
            resp_data = resp.json()
        else:
            break

    return repositories