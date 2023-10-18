def build_full_day_ips(query, period_start, period_end):
    """Method to build an IP list for the case 1

    when the IP was allocated before the period start
    and is still allocated after the period end.
    This method only looks at public IPv4 addresses.
    """
    # Filter out only IPv4 that have not been deallocated
    ip_list = query.\
        filter(models.IPAddress.version == 4L).\
        filter(models.IPAddress.network_id == PUBLIC_NETWORK_ID).\
        filter(models.IPAddress.used_by_tenant_id is not None).\
        filter(models.IPAddress.allocated_at != null()).\
        filter(models.IPAddress.allocated_at < period_start).\
        filter(or_(models.IPAddress._deallocated is False,
                   models.IPAddress.deallocated_at == null(),
                   models.IPAddress.deallocated_at >= period_end)).all()

    return ip_list