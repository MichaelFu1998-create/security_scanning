def get_name():
    """
    Retrieves the instance name associated with the current host string.
    """
    if env.vm_type == EC2:
        for instance in get_all_running_ec2_instances():
            if env.host_string == instance.public_dns_name:
                name = instance.tags.get(env.vm_name_tag)
                return name
    else:
        raise NotImplementedError