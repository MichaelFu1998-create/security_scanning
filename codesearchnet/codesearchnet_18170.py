def balance(ctx):
    """
    Show Zebra balance.

    Like the hours balance, vacation left, etc.
    """
    backend = plugins_registry.get_backends_by_class(ZebraBackend)[0]

    timesheet_collection = get_timesheet_collection_for_context(ctx, None)
    hours_to_be_pushed = timesheet_collection.get_hours(pushed=False, ignored=False, unmapped=False)

    today = datetime.date.today()
    user_info = backend.get_user_info()
    timesheets = backend.get_timesheets(get_first_dow(today), get_last_dow(today))
    total_duration = sum([float(timesheet['time']) for timesheet in timesheets])

    vacation = hours_to_days(user_info['vacation']['difference'])
    vacation_balance = '{} days, {:.2f} hours'.format(*vacation)

    hours_balance = user_info['hours']['hours']['balance']

    click.echo("Hours balance: {}".format(signed_number(hours_balance)))
    click.echo("Hours balance after push: {}".format(signed_number(hours_balance + hours_to_be_pushed)))
    click.echo("Hours done this week: {:.2f}".format(total_duration))
    click.echo("Vacation left: {}".format(vacation_balance))