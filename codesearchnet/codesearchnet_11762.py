def get_or_create_ec2_key_pair(name=None, verbose=1):
    """
    Creates and saves an EC2 key pair to a local PEM file.
    """
    verbose = int(verbose)
    name = name or env.vm_ec2_keypair_name
    pem_path = 'roles/%s/%s.pem' % (env.ROLE, name)
    conn = get_ec2_connection()
    kp = conn.get_key_pair(name)
    if kp:
        print('Key pair %s already exists.' % name)
    else:
        # Note, we only get the private key during creation.
        # If we don't save it here, it's lost forever.
        kp = conn.create_key_pair(name)
        open(pem_path, 'wb').write(kp.material)
        os.system('chmod 600 %s' % pem_path)
        print('Key pair %s created.' % name)
    #return kp
    return pem_path