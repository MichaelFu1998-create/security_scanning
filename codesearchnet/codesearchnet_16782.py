def execute(helper, config, args):
    """
    Lists environments
    """
    envs = config.get('app', {}).get('environments', [])
    out("Parsed environments:")
    for name, conf in list(envs.items()):
        out('\t'+name)
    envs = helper.get_environments()
    out("Deployed environments:")
    for env in envs:
        if env['Status'] != 'Terminated':
            out('\t'+str(env['EnvironmentName'])+' ('+str(env['Status'])+', '+str(env['CNAME'])+')')