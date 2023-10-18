def freeze(ctx, local=False):
    """Freeze currently installed requirements."""
    cmd = 'pip --disable-pip-version-check freeze{}'.format(' --local' if local else '')
    frozen = ctx.run(cmd, hide='out').stdout.replace('\x1b', '#')
    with io.open('frozen-requirements.txt', 'w', encoding='ascii') as out:
        out.write("# Requirements frozen by 'pip freeze' on {}\n".format(isodate()))
        out.write(frozen)
    notify.info("Frozen {} requirements.".format(len(frozen.splitlines()),))