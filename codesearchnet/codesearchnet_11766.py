def delete(name=None, group=None, release=None, except_release=None,
    dryrun=1, verbose=1):
    """
    Permanently erase one or more VM instances from existence.
    """

    verbose = int(verbose)

    if env.vm_type == EC2:
        conn = get_ec2_connection()

        instances = list_instances(
            name=name,
            group=group,
            release=release,
            except_release=except_release,
        )

        for instance_name, instance_data in instances.items():
            public_dns_name = instance_data['public_dns_name']
            print('\nDeleting %s (%s)...' \
                % (instance_name, instance_data['id']))
            if not get_dryrun():
                conn.terminate_instances(instance_ids=[instance_data['id']])

            # Clear host key on localhost.
            known_hosts = os.path.expanduser('~/.ssh/known_hosts')
            cmd = 'ssh-keygen -f "%s" -R %s' % (known_hosts, public_dns_name)
            local_or_dryrun(cmd)

    else:
        raise NotImplementedError