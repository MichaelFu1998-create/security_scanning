def main(notify, hour, minute):
    """Runs billing report. Optionally sends notifications to billing"""

    # Read the config file and get the admin context
    config_opts = ['--config-file', '/etc/neutron/neutron.conf']
    config.init(config_opts)
    # Have to load the billing module _after_ config is parsed so
    # that we get the right network strategy
    network_strategy.STRATEGY.load()
    billing.PUBLIC_NETWORK_ID = network_strategy.STRATEGY.get_public_net_id()
    config.setup_logging()
    context = neutron_context.get_admin_context()

    # A query to get all IPAddress objects from the db
    query = context.session.query(models.IPAddress)

    (period_start, period_end) = billing.calc_periods(hour, minute)

    full_day_ips = billing.build_full_day_ips(query,
                                              period_start,
                                              period_end)
    partial_day_ips = billing.build_partial_day_ips(query,
                                                    period_start,
                                                    period_end)

    if notify:
        # '==================== Full Day ============================='
        for ipaddress in full_day_ips:
            click.echo('start: {}, end: {}'.format(period_start, period_end))
            payload = billing.build_payload(ipaddress,
                                            billing.IP_EXISTS,
                                            start_time=period_start,
                                            end_time=period_end)
            billing.do_notify(context,
                              billing.IP_EXISTS,
                              payload)
        # '==================== Part Day ============================='
        for ipaddress in partial_day_ips:
            click.echo('start: {}, end: {}'.format(period_start, period_end))
            payload = billing.build_payload(ipaddress,
                                            billing.IP_EXISTS,
                                            start_time=ipaddress.allocated_at,
                                            end_time=period_end)
            billing.do_notify(context,
                              billing.IP_EXISTS,
                              payload)
    else:
        click.echo('Case 1 ({}):\n'.format(len(full_day_ips)))
        for ipaddress in full_day_ips:
            pp(billing.build_payload(ipaddress,
                                     billing.IP_EXISTS,
                                     start_time=period_start,
                                     end_time=period_end))

        click.echo('\n===============================================\n')

        click.echo('Case 2 ({}):\n'.format(len(partial_day_ips)))
        for ipaddress in partial_day_ips:
            pp(billing.build_payload(ipaddress,
                                     billing.IP_EXISTS,
                                     start_time=ipaddress.allocated_at,
                                     end_time=period_end))