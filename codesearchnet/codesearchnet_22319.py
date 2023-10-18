def scaffold():
    """Start a new site."""
    click.echo("A whole new site? Awesome.")
    title = click.prompt("What's the title?")
    url = click.prompt("Great. What's url? http://")

    # Make sure that title doesn't exist.
    click.echo("Got it. Creating %s..." % url)