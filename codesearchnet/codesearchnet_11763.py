def get_or_create_ec2_instance(name=None, group=None, release=None, verbose=0, backend_opts=None):
    """
    Creates a new EC2 instance.

    You should normally run get_or_create() instead of directly calling this.
    """
    from burlap.common import shelf, OrderedDict
    from boto.exception import EC2ResponseError

    assert name, "A name must be specified."

    backend_opts = backend_opts or {}

    verbose = int(verbose)

    conn = get_ec2_connection()

    security_groups = get_or_create_ec2_security_groups()
    security_group_ids = [_.id for _ in security_groups]
    if verbose:
        print('security_groups:', security_group_ids)

    pem_path = get_or_create_ec2_key_pair()

    assert env.vm_ec2_ami, 'No AMI specified.'
    print('Creating EC2 instance from %s...' % (env.vm_ec2_ami,))
    print(env.vm_ec2_zone)
    opts = backend_opts.get('run_instances', {})
    reservation = conn.run_instances(
        env.vm_ec2_ami,
        key_name=env.vm_ec2_keypair_name,
        #security_groups=env.vm_ec2_selected_security_groups,#conflicts with subnet_id?!
        security_group_ids=security_group_ids,
        placement=env.vm_ec2_zone,
        instance_type=env.vm_ec2_instance_type,
        subnet_id=env.vm_ec2_subnet_id,
        **opts
    )
    instance = reservation.instances[0]

    # Name new instance.
    # Note, creation is not instantious, so we may have to wait for a moment
    # before we can access it.
    while 1:
        try:
            if name:
                instance.add_tag(env.vm_name_tag, name)
            if group:
                instance.add_tag(env.vm_group_tag, group)
            if release:
                instance.add_tag(env.vm_release_tag, release)
            break
        except EC2ResponseError as e:
            #print('Unable to set tag: %s' % e)
            print('Waiting for the instance to be created...')
            if verbose:
                print(e)
            time.sleep(3)

    # Assign IP.
    allocation_id = None
    if env.vm_ec2_use_elastic_ip:
        # Initialize name/ip mapping since we can't tag elastic IPs.
        shelf.setdefault('vm_elastic_ip_mappings', OrderedDict())
        vm_elastic_ip_mappings = shelf.get('vm_elastic_ip_mappings')
        elastic_ip = vm_elastic_ip_mappings.get(name)
        if not elastic_ip:
            print('Allocating new elastic IP address...')
            addr = conn.allocate_address(domain=env.vm_ec2_allocate_address_domain)
            #allocation_id = addr.allocation_id
            #print('allocation_id:',allocation_id)
            elastic_ip = addr.public_ip
            print('Allocated address %s.' % elastic_ip)
            vm_elastic_ip_mappings[name] = str(elastic_ip)
            shelf.set('vm_elastic_ip_mappings', vm_elastic_ip_mappings)
            #conn.get_all_addresses()

        # Lookup allocation_id.
        all_eips = conn.get_all_addresses()
        for eip in all_eips:
            if elastic_ip == eip.public_ip:
                allocation_id = eip.allocation_id
                break
        print('allocation_id:', allocation_id)

        while 1:
            try:
                conn.associate_address(
                    instance_id=instance.id,
                    #public_ip=elastic_ip,
                    allocation_id=allocation_id, # needed for VPC instances
                    )
                print('IP address associated!')
                break
            except EC2ResponseError as e:
                #print('Unable to assign IP: %s' % e)
                print('Waiting to associate IP address...')
                if verbose:
                    print(e)
                time.sleep(3)

    # Confirm public DNS name was assigned.
    while 1:
        try:
            instance = get_all_ec2_instances(instance_ids=[instance.id])[0]
            #assert instance.public_dns_name, 'No public DNS name found!'
            if instance.public_dns_name:
                break
        except Exception as e:
            print('error:', e)
        except SystemExit as e:
            print('systemexit:', e)
        print('Waiting for public DNS name to be assigned...')
        time.sleep(3)

    # Confirm we can SSH into the server.
    #TODO:better handle timeouts? try/except doesn't really work?
    env.connection_attempts = 10
    while 1:
        try:
            with settings(warn_only=True):
                env.host_string = instance.public_dns_name
                ret = run_or_dryrun('who -b')
                #print 'ret.return_code:',ret.return_code
                if not ret.return_code:
                    break
        except Exception as e:
            print('error:', e)
        except SystemExit as e:
            print('systemexit:', e)
        print('Waiting for sshd to accept connections...')
        time.sleep(3)

    print("")
    print("Login with: ssh -o StrictHostKeyChecking=no -i %s %s@%s" \
        % (pem_path, env.user, instance.public_dns_name))
    print("OR")
    print("fab %(ROLE)s:hostname=%(name)s shell" % dict(name=name, ROLE=env.ROLE))

    ip = socket.gethostbyname(instance.public_dns_name)
    print("")
    print("""Example hosts entry:)
%(ip)s    www.mydomain.com # %(name)s""" % dict(ip=ip, name=name))
    return instance