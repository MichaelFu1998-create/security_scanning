def list_instances(show=1, name=None, group=None, release=None, except_release=None):
    """
    Retrieves all virtual machines instances in the current environment.
    """
    from burlap.common import shelf, OrderedDict, get_verbose

    verbose = get_verbose()
    require('vm_type', 'vm_group')
    assert env.vm_type, 'No VM type specified.'
    env.vm_type = (env.vm_type or '').lower()
    _name = name
    _group = group
    _release = release
    if verbose:
        print('name=%s, group=%s, release=%s' % (_name, _group, _release))

    env.vm_elastic_ip_mappings = shelf.get('vm_elastic_ip_mappings')

    data = type(env)()
    if env.vm_type == EC2:
        if verbose:
            print('Checking EC2...')
        for instance in get_all_running_ec2_instances():
            name = instance.tags.get(env.vm_name_tag)
            group = instance.tags.get(env.vm_group_tag)
            release = instance.tags.get(env.vm_release_tag)
            if env.vm_group and env.vm_group != group:
                if verbose:
                    print(('Skipping instance %s because its group "%s" '
                        'does not match env.vm_group "%s".') \
                            % (instance.public_dns_name, group, env.vm_group))
                continue
            if _group and group != _group:
                if verbose:
                    print(('Skipping instance %s because its group "%s" '
                        'does not match local group "%s".') \
                            % (instance.public_dns_name, group, _group))
                continue
            if _name and name != _name:
                if verbose:
                    print(('Skipping instance %s because its name "%s" '
                        'does not match name "%s".') \
                            % (instance.public_dns_name, name, _name))
                continue
            if _release and release != _release:
                if verbose:
                    print(('Skipping instance %s because its release "%s" '
                        'does not match release "%s".') \
                            % (instance.public_dns_name, release, _release))
                continue
            if except_release and release == except_release:
                continue
            if verbose:
                print('Adding instance %s (%s).' \
                    % (name, instance.public_dns_name))
            data.setdefault(name, type(env)())
            data[name]['id'] = instance.id
            data[name]['public_dns_name'] = instance.public_dns_name
            if verbose:
                print('Public DNS: %s' % instance.public_dns_name)

            if env.vm_elastic_ip_mappings and name in env.vm_elastic_ip_mappings:
                data[name]['ip'] = env.vm_elastic_ip_mappings[name]
            else:
                data[name]['ip'] = socket.gethostbyname(instance.public_dns_name)

        if int(show):
            pprint(data, indent=4)
        return data
    elif env.vm_type == KVM:
        #virsh list
        pass
    else:
        raise NotImplementedError