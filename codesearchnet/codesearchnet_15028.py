def sphinx(ctx, browse=False, clean=False, watchdog=False, kill=False, status=False, opts=''):
    """Build Sphinx docs."""
    cfg = config.load()

    if kill or status:
        if not watchdogctl(ctx, kill=kill):
            notify.info("No process bound to port {}".format(ctx.rituals.docs.watchdog.port))
        return

    if clean:
        ctx.run("invoke clean --docs")

    # Convert markdown files, if applicable
    for basename in ('README', 'CONTRIBUTING'):
        markdown = cfg.rootjoin(basename + '.md')
        if os.path.exists(markdown):
            try:
                import pypandoc
            except ImportError as exc:
                notify.warning("Can't import 'pandoc' ({})".format(exc))
                break
            else:
                pypandoc.convert(markdown, 'rst', outputfile=os.path.join(ctx.rituals.docs.sources, basename + '.rst'))

    # LICENSE file
    if os.path.exists('LICENSE'):
        with io.open('LICENSE', 'r') as inp:
            license_text = inp.read()
            try:
                _, copyright_text = cfg.project['long_description'].split('Copyright', 1)
            except (KeyError, ValueError):
                copyright_text = cfg.project.get('license', 'N/A')
            with io.open(os.path.join(ctx.rituals.docs.sources, 'LICENSE.rst'), 'w') as out:
                out.write(
                    'Software License\n'
                    '================\n'
                    '\n'
                    '    Copyright {}\n'
                    '\n'
                    'Full License Text\n'
                    '-----------------\n'
                    '\n'
                    '::\n'
                    '\n'
                    .format(copyright_text)
                )
                license_text = textwrap.dedent(license_text)
                license_text = '\n    '.join(license_text.splitlines())
                out.write('    {}\n'.format(license_text))

    # Build API docs
    if cfg.project.get('packages') and str(ctx.rituals.docs.apidoc).lower()[:1] in 't1y':
        cmd = ['sphinx-apidoc', '-o', 'api', '-f', '-M']
        for package in cfg.project.packages:
            if '.' not in package:
                cmd.append(cfg.srcjoin(package))
        with pushd(ctx.rituals.docs.sources):
            ctx.run(' '.join(cmd))

    # Auto build?
    cmd = ['sphinx-build', '-b', 'html']
    if opts:
        cmd.append(opts)
    cmd.extend(['.', ctx.rituals.docs.build])
    index_url = index_file = os.path.join(ctx.rituals.docs.sources, ctx.rituals.docs.build, 'index.html')
    if watchdog:
        watchdogctl(ctx, kill=True)
        cmd[0:1] = ['nohup', 'sphinx-autobuild']
        cmd.extend([
               '-H', ctx.rituals.docs.watchdog.host,
               '-p', '{}'.format(ctx.rituals.docs.watchdog.port),
               "-i'{}'".format('*~'),
               "-i'{}'".format('.*'),
               "-i'{}'".format('*.log'),
               ">watchdog.log", "2>&1", "&",
        ])
        index_url = "http://{}:{}/".format(ctx.rituals.docs.watchdog.host, ctx.rituals.docs.watchdog.port)

    # Build docs
    notify.info("Starting Sphinx {}build...".format('auto' if watchdog else ''))
    with pushd(ctx.rituals.docs.sources):
        ctx.run(' '.join(cmd), pty=not watchdog)

    # Wait for watchdog to bind to listening port
    if watchdog:
        def activity(what=None, i=None):
            "Helper"
            if i is None:
                sys.stdout.write(what + '\n')
            else:
                sys.stdout.write(' {}  Waiting for {}\r'.format(r'\|/-'[i % 4], what or 'something'))
            sys.stdout.flush()

        for i in range(60):
            activity('server start', i)
            if watchdogctl(ctx):
                activity('OK')
                break
            time.sleep(1)
        else:
            activity('ERR')

        # trigger first build
        if os.path.exists(os.path.join(ctx.rituals.docs.sources, 'index.rst')):
            os.utime(os.path.join(ctx.rituals.docs.sources, 'index.rst'), None)

        for i in range(60):
            activity('HTML index file', i)
            if os.path.exists(index_file):
                activity('OK')
                break
            time.sleep(1)
        else:
            activity('ERR')

    # Open in browser?
    if browse:
        time.sleep(1)
        webbrowser.open_new_tab(index_url)