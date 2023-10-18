def lint(context):
    """Looks for errors in source code of your blog"""

    config = context.obj
    try:
        run('flake8 {dir} --exclude={exclude}'.format(
            dir=config['CWD'],
            exclude=','.join(EXCLUDE),
        ))
    except SubprocessError:
        context.exit(1)