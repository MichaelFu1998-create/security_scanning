def run():
    """Fetches changes and applies them to VIFs periodically

    Process as of RM11449:
    * Get all groups from redis
    * Fetch ALL VIFs from Xen
    * Walk ALL VIFs and partition them into added, updated and removed
    * Walk the final "modified" VIFs list and apply flows to each
    """
    groups_client = sg_cli.SecurityGroupsClient()
    xapi_client = xapi.XapiClient()

    interfaces = set()
    while True:
        try:
            interfaces = xapi_client.get_interfaces()
        except Exception:
            LOG.exception("Unable to get instances/interfaces from xapi")
            _sleep()
            continue

        try:
            sg_states = groups_client.get_security_group_states(interfaces)
            new_sg, updated_sg, removed_sg = partition_vifs(xapi_client,
                                                            interfaces,
                                                            sg_states)
            xapi_client.update_interfaces(new_sg, updated_sg, removed_sg)
            groups_to_ack = [v for v in new_sg + updated_sg if v.success]
            # NOTE(quade): This solves a race condition where a security group
            # rule may have changed between the time the sg_states were called
            # and when they were officially ack'd. It functions as a compare
            # and set. This is a fix until we get onto a proper messaging
            # queue. NCP-2287
            sg_sts_curr = groups_client.get_security_group_states(interfaces)
            groups_to_ack = get_groups_to_ack(groups_to_ack, sg_states,
                                              sg_sts_curr)
            # This list will contain all the security group rules that do not
            # match
            ack_groups(groups_client, groups_to_ack)

        except Exception:
            LOG.exception("Unable to get security groups from registry and "
                          "apply them to xapi")
            _sleep()
            continue

        _sleep()