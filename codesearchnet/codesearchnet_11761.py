def get_or_create_ec2_security_groups(names=None, verbose=1):
    """
    Creates a security group opening 22, 80 and 443
    """
    verbose = int(verbose)

    if verbose:
        print('Creating EC2 security groups...')

    conn = get_ec2_connection()

    if isinstance(names, six.string_types):
        names = names.split(',')
    names = names or env.vm_ec2_selected_security_groups
    if verbose:
        print('Group names:', names)

    ret = []
    for name in names:
        try:
            group_id = get_ec2_security_group_id(name)
            if verbose:
                print('group_id:', group_id)
            #group = conn.get_all_security_groups(groupnames=[name])[0]
            # Note, groups in a VPC can't be referred to by name?
            group = conn.get_all_security_groups(group_ids=[group_id])[0]
        except boto.exception.EC2ResponseError as e:
            if verbose:
                print(e)
            group = get_ec2_connection().create_security_group(
                name,
                name,
                vpc_id=env.vm_ec2_vpc_id,
            )
            print('group_id:', group.id)
            set_ec2_security_group_id(name, group.id)
        ret.append(group)

        # Find existing rules.
        actual_sets = set()
        for rule in list(group.rules):
            ip_protocol = rule.ip_protocol
            from_port = rule.from_port
            to_port = rule.to_port
            for cidr_ip in rule.grants:
                #print('Revoking:', ip_protocol, from_port, to_port, cidr_ip)
                #group.revoke(ip_protocol, from_port, to_port, cidr_ip)
                rule_groups = ((rule.groups and rule.groups.split(',')) or [None])
                for src_group in rule_groups:
                    src_group = (src_group or '').strip()
                    if src_group:
                        actual_sets.add((ip_protocol, from_port, to_port, str(cidr_ip), src_group))
                    else:
                        actual_sets.add((ip_protocol, from_port, to_port, str(cidr_ip)))

        # Find actual rules.
        expected_sets = set()
        for authorization in env.vm_ec2_available_security_groups.get(name, []):
            if verbose:
                print('authorization:', authorization)
            if len(authorization) == 4 or (len(authorization) == 5 and not (authorization[-1] or '').strip()):
                src_group = None
                ip_protocol, from_port, to_port, cidr_ip = authorization[:4]
                if cidr_ip:
                    expected_sets.add((ip_protocol, str(from_port), str(to_port), cidr_ip))
            else:
                ip_protocol, from_port, to_port, cidr_ip, src_group = authorization
                if cidr_ip:
                    expected_sets.add((ip_protocol, str(from_port), str(to_port), cidr_ip, src_group))

        # Calculate differences and update rules if we own the group.
        if env.vm_ec2_security_group_owner:
            if verbose:
                print('expected_sets:')
                print(expected_sets)
                print('actual_sets:')
                print(actual_sets)
            del_sets = actual_sets.difference(expected_sets)
            if verbose:
                print('del_sets:')
                print(del_sets)
            add_sets = expected_sets.difference(actual_sets)
            if verbose:
                print('add_sets:')
                print(add_sets)

            # Revoke deleted.
            for auth in del_sets:
                print(len(auth))
                print('revoking:', auth)
                group.revoke(*auth)

            # Create fresh rules.
            for auth in add_sets:
                print('authorizing:', auth)
                group.authorize(*auth)

    return ret