def activate(paths, skip_local, skip_shared):
    '''Activate an environment'''


    if not paths:
        ctx = click.get_current_context()
        if cpenv.get_active_env():
            ctx.invoke(info)
            return

        click.echo(ctx.get_help())
        examples = (
            '\nExamples: \n'
            '    cpenv activate my_env\n'
            '    cpenv activate ./relative/path/to/my_env\n'
            '    cpenv activate my_env my_module\n'
        )
        click.echo(examples)
        return

    if skip_local:
        cpenv.module_resolvers.remove(cpenv.resolver.module_resolver)
        cpenv.module_resolvers.remove(cpenv.resolver.active_env_module_resolver)

    if skip_shared:
        cpenv.module_resolvers.remove(cpenv.resolver.modules_path_resolver)

    try:
        r = cpenv.resolve(*paths)
    except cpenv.ResolveError as e:
        click.echo('\n' + str(e))
        return

    resolved = set(r.resolved)
    active_modules = set()
    env = cpenv.get_active_env()
    if env:
        active_modules.add(env)
    active_modules.update(cpenv.get_active_modules())

    new_modules = resolved - active_modules
    old_modules = active_modules & resolved

    if old_modules and not new_modules:
        click.echo(
            '\nModules already active: '
            + bold(' '.join([obj.name for obj in old_modules]))
        )
        return

    if env and contains_env(new_modules):
        click.echo('\nUse bold(exit) to leave your active environment first.')
        return

    click.echo('\nResolved the following modules...')
    click.echo(format_objects(r.resolved))
    r.activate()
    click.echo(blue('\nLaunching subshell...'))

    modules = sorted(resolved | active_modules, key=_type_and_name)
    prompt = ':'.join([obj.name for obj in modules])
    shell.launch(prompt)