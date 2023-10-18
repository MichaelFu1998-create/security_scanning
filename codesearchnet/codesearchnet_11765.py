def get_or_create(name=None, group=None, config=None, extra=0, verbose=0, backend_opts=None):
    """
    Creates a virtual machine instance.
    """
    require('vm_type', 'vm_group')

    backend_opts = backend_opts or {}

    verbose = int(verbose)
    extra = int(extra)

    if config:
        config_fn = common.find_template(config)
        config = yaml.load(open(config_fn))
        env.update(config)

    env.vm_type = (env.vm_type or '').lower()
    assert env.vm_type, 'No VM type specified.'

    group = group or env.vm_group
    assert group, 'No VM group specified.'

    ret = exists(name=name, group=group)
    if not extra and ret:
        if verbose:
            print('VM %s:%s exists.' % (name, group))
        return ret

    today = datetime.date.today()
    release = int('%i%02i%02i' % (today.year, today.month, today.day))

    if not name:
        existing_instances = list_instances(
            group=group,
            release=release,
            verbose=verbose)
        name = env.vm_name_template.format(index=len(existing_instances)+1)

    if env.vm_type == EC2:
        return get_or_create_ec2_instance(
            name=name,
            group=group,
            release=release,
            verbose=verbose,
            backend_opts=backend_opts)
    else:
        raise NotImplementedError