def get_used_ips(session, **kwargs):
    """Returns dictionary with keys segment_id and value used IPs count.

    Used IP address count is determined by:
    - allocated IPs
    - deallocated IPs whose `deallocated_at` is within the `reuse_after`
    window compared to the present time, excluding IPs that are accounted for
    in the current IP policy (because IP policy is mutable and deallocated IPs
    are not checked nor deleted on IP policy creation, thus deallocated IPs
    that don't fit the current IP policy can exist in the neutron database).
    """
    LOG.debug("Getting used IPs...")
    with session.begin():
        query = session.query(
            models.Subnet.segment_id,
            func.count(models.IPAddress.address))
        query = query.group_by(models.Subnet.segment_id)
        query = _filter(query, **kwargs)

        reuse_window = timeutils.utcnow() - datetime.timedelta(
            seconds=cfg.CONF.QUARK.ipam_reuse_after)
        # NOTE(asadoughi): This is an outer join instead of a regular join
        # to include subnets with zero IP addresses in the database.
        query = query.outerjoin(
            models.IPAddress,
            and_(models.Subnet.id == models.IPAddress.subnet_id,
                 or_(not_(models.IPAddress.lock_id.is_(None)),
                     models.IPAddress._deallocated.is_(None),
                     models.IPAddress._deallocated == 0,
                     models.IPAddress.deallocated_at > reuse_window)))

        query = query.outerjoin(
            models.IPPolicyCIDR,
            and_(
                models.Subnet.ip_policy_id == models.IPPolicyCIDR.ip_policy_id,
                models.IPAddress.address >= models.IPPolicyCIDR.first_ip,
                models.IPAddress.address <= models.IPPolicyCIDR.last_ip))
        # NOTE(asadoughi): (address is allocated) OR
        # (address is deallocated and not inside subnet's IP policy)
        query = query.filter(or_(
            models.IPAddress._deallocated.is_(None),
            models.IPAddress._deallocated == 0,
            models.IPPolicyCIDR.id.is_(None)))

        ret = ((segment_id, address_count)
               for segment_id, address_count in query.all())
        return dict(ret)