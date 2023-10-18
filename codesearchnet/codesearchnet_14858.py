def make_case2(context):
    """This is a helper method for testing.

    When run with the current context, it will create a case 2 entries
    in the database. See top of file for what case 2 is.
    """
    query = context.session.query(models.IPAddress)
    period_start, period_end = billing.calc_periods()
    ip_list = billing.build_full_day_ips(query, period_start, period_end)
    import random
    ind = random.randint(0, len(ip_list) - 1)
    address = ip_list[ind]
    address.allocated_at = datetime.datetime.utcnow() -\
        datetime.timedelta(days=1)
    context.session.add(address)
    context.session.flush()