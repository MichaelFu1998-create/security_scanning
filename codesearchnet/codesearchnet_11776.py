def disable_attribute_or_dryrun(*args, **kwargs):
    """
    Comments-out a line containing an attribute.
    The inverse of enable_attribute_or_dryrun().
    """
    dryrun = get_dryrun(kwargs.get('dryrun'))

    if 'dryrun' in kwargs:
        del kwargs['dryrun']

    use_sudo = kwargs.pop('use_sudo', False)
    run_cmd = sudo_or_dryrun if use_sudo else run_or_dryrun
    run_cmd_str = 'sudo' if use_sudo else 'run'

    key = args[0] if len(args) >= 1 else kwargs.pop('key')

    filename = args[1] if len(args) >= 2 else kwargs.pop('filename')

    comment_pattern = args[2] if len(args) >= 3 else kwargs.pop('comment_pattern', r'#\s*')

    equals_pattern = args[3] if len(args) >= 4 else kwargs.pop('equals_pattern', r'\s*=\s*')

    equals_literal = args[4] if len(args) >= 5 else kwargs.pop('equals_pattern', '=')

    context = dict(
        key=key,
        uncommented_literal='%s%s' % (key, equals_literal), # key=value
        uncommented_pattern='%s%s' % (key, equals_pattern), # key = value
        uncommented_pattern_partial='^%s%s[^\\n]*' % (key, equals_pattern), # key=
        commented_pattern='%s%s%s' % (comment_pattern, key, equals_pattern), # #key=value
        commented_pattern_partial='^%s%s%s[^\\n]*' % (comment_pattern, key, equals_pattern), # #key=
        filename=filename,
        backup=filename+'.bak',
        comment_pattern=comment_pattern,
        equals_pattern=equals_pattern,
    )

    cmds = [
        # Replace partial un-commented text with full commented text.
        'sed -i -r -e "s/{uncommented_pattern_partial}//g" {filename}'.format(**context),
    ]

    if dryrun:
        for cmd in cmds:
            if BURLAP_COMMAND_PREFIX:
                print('%s %s: %s' % (render_command_prefix(), run_cmd_str, cmd))
            else:
                print(cmd)
    else:
        for cmd in cmds:
#             print('enable attr:', cmd)
            run_cmd(cmd)