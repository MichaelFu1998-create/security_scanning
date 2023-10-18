def version():
    """Display full version information."""

    # Print out the current version of Tower CLI.
    click.echo('Tower CLI %s' % __version__)

    # Print out the current API version of the current code base.
    click.echo('API %s' % CUR_API_VERSION)

    # Attempt to connect to the Ansible Tower server.
    # If we succeed, print a version; if not, generate a failure.
    try:
        r = client.get('/config/')
    except RequestException as ex:
        raise exc.TowerCLIError('Could not connect to Ansible Tower.\n%s' %
                                six.text_type(ex))
    config = r.json()
    license = config.get('license_info', {}).get('license_type', 'open')
    if license == 'open':
        server_type = 'AWX'
    else:
        server_type = 'Ansible Tower'
    click.echo('%s %s' % (server_type, config['version']))

    # Print out Ansible version of server
    click.echo('Ansible %s' % config['ansible_version'])