def parse_env_config(config, env_name):
    """
    Parses an environment config
    """
    all_env = get(config, 'app.all_environments', {})
    env = get(config, 'app.environments.' + str(env_name), {})
    return merge_dict(all_env, env)