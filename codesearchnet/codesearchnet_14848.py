def get_unused_ips(session, used_ips_counts, **kwargs):
    """Returns dictionary with key segment_id, and value unused IPs count.

    Unused IP address count is determined by:
    - adding subnet's cidr's size
    - subtracting IP policy exclusions on subnet
    - subtracting used ips per segment
    """
    LOG.debug("Getting unused IPs...")
    with session.begin():
        query = session.query(
            models.Subnet.segment_id,
            models.Subnet)
        query = _filter(query, **kwargs)
        query = query.group_by(models.Subnet.segment_id, models.Subnet.id)

        ret = defaultdict(int)
        for segment_id, subnet in query.all():
            net_size = netaddr.IPNetwork(subnet._cidr).size
            ip_policy = subnet["ip_policy"] or {"size": 0}
            ret[segment_id] += net_size - ip_policy["size"]

        for segment_id in used_ips_counts:
            ret[segment_id] -= used_ips_counts[segment_id]

        return ret