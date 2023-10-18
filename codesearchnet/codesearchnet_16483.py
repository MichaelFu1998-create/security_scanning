def dashboard(yes, url):
    """Open dashboard in browser."""
    dashboard_url = "{}/app".format(PolyaxonClient().api_config.http_host)
    if url:
        click.echo(dashboard_url)
        sys.exit(0)
    if not yes:
        click.confirm('Dashboard page will now open in your browser. Continue?',
                      abort=True, default=True)

    click.launch(dashboard_url)