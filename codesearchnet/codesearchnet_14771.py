def partition_vifs(xapi_client, interfaces, security_group_states):
    """Splits VIFs into three explicit categories and one implicit

    Added - Groups exist in Redis that have not been ack'd and the VIF
            is not tagged.
            Action: Tag the VIF and apply flows
    Updated - Groups exist in Redis that have not been ack'd and the VIF
              is already tagged
              Action: Do not tag the VIF, do apply flows
    Removed - Groups do NOT exist in Redis but the VIF is tagged
              Action: Untag the VIF, apply default flows
    Self-Heal - Groups are ack'd in Redis but the VIF is untagged. We treat
                this case as if it were an "added" group.
                Action: Tag the VIF and apply flows
    NOOP - The VIF is not tagged and there are no matching groups in Redis.
           This is our implicit category
           Action: Do nothing
    """
    added = []
    updated = []
    removed = []

    for vif in interfaces:
        # Quark should not action on isonet vifs in regions that use FLIP
        if ('floating_ip' in CONF.QUARK.environment_capabilities and
                is_isonet_vif(vif)):
            continue

        vif_has_groups = vif in security_group_states
        if vif.tagged and vif_has_groups and\
                security_group_states[vif][sg_cli.SECURITY_GROUP_ACK]:
            # Already ack'd these groups and VIF is tagged, reapply.
            # If it's not tagged, fall through and have it self-heal
            continue

        if vif.tagged:
            if vif_has_groups:
                updated.append(vif)
            else:
                removed.append(vif)
        else:
            if vif_has_groups:
                added.append(vif)
            # if not tagged and no groups, skip

    return added, updated, removed