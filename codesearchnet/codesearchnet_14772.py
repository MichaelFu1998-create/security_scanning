def get_groups_to_ack(groups_to_ack, init_sg_states, curr_sg_states):
    """Compares initial security group rules with current sg rules.

    Given the groups that were successfully returned from
        xapi_client.update_interfaces call, compare initial and current
        security group rules to determine if an update occurred during
        the window that the xapi_client.update_interfaces was executing.
        Return a list of vifs whose security group rules have not changed.
    """
    security_groups_changed = []
    # Compare current security group rules with initial rules.
    for vif in groups_to_ack:
        initial_state = init_sg_states[vif][sg_cli.SECURITY_GROUP_HASH_ATTR]
        current_state = curr_sg_states[vif][sg_cli.SECURITY_GROUP_HASH_ATTR]
        bad_match_msg = ('security group rules were changed for vif "%s" while'
                         ' executing xapi_client.update_interfaces.'
                         ' Will not ack rule.' % vif)
        # If lists are different lengths, they're automatically different.
        if len(initial_state) != len(current_state):
            security_groups_changed.append(vif)
            LOG.info(bad_match_msg)
        elif len(initial_state) > 0:
            # Compare rules in equal length lists.
            for rule in current_state:
                if rule not in initial_state:
                    security_groups_changed.append(vif)
                    LOG.info(bad_match_msg)
                    break

    # Only ack groups whose rules have not changed since update. If
    # rules do not match, do not add them to ret so the change
    # can be picked up on the next cycle.
    ret = [group for group in groups_to_ack
           if group not in security_groups_changed]
    return ret