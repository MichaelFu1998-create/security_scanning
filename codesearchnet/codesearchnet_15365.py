def _formatter_callback_factory():  # pragma: no cover
    """Returns a list of includes to be given to `cnxepub.collation.collate`.

    """
    includes = []
    exercise_url_template = '{baseUrl}/api/exercises?q={field}:"{{itemCode}}"'
    settings = get_current_registry().settings
    exercise_base_url = settings.get('embeddables.exercise.base_url', None)
    exercise_matches = [match.split(',', 1) for match in aslist(
        settings.get('embeddables.exercise.match', ''), flatten=False)]
    exercise_token = settings.get('embeddables.exercise.token', None)
    mathml_url = settings.get('mathmlcloud.url', None)
    memcache_servers = settings.get('memcache_servers')
    if memcache_servers:
        memcache_servers = memcache_servers.split()
    else:
        memcache_servers = None

    if exercise_base_url and exercise_matches:
        mc_client = None
        if memcache_servers:
            mc_client = memcache.Client(memcache_servers, debug=0)
        for (exercise_match, exercise_field) in exercise_matches:
            template = exercise_url_template.format(
                baseUrl=exercise_base_url, field=exercise_field)
            includes.append(exercise_callback_factory(exercise_match,
                                                      template,
                                                      mc_client,
                                                      exercise_token,
                                                      mathml_url))
    return includes