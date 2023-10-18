def pprint(value):
    """Prints as formatted JSON"""
    click.echo(
        json.dumps(value,
                   sort_keys=True,
                   indent=4,
                   separators=(',', ': ')))