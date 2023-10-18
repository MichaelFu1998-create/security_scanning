def clear(skip):
    """Clear all caches."""
    for name in sorted(MODULES):
        if name in skip:
            continue
        click.secho(f'clearing cache for {name}', fg='cyan', bold=True)
        clear_cache(name)