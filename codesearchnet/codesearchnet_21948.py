def get_upcoming_events_count(days=14, featured=False):
    """
    Returns count of upcoming events for a given number of days, either featured or all
    Usage:
    {% get_upcoming_events_count DAYS as events_count %}
    with days being the number of days you want, or 5 by default
    """
    from happenings.models import Event
    start_period = today - datetime.timedelta(days=2)
    end_period = today + datetime.timedelta(days=days)
    if featured:
        return Event.objects.filter(
            featured=True,
            start_date__gte=start_period,
            start_date__lte=end_period
        ).count()
    return Event.objects.filter(start_date__gte=start_period, start_date__lte=end_period).count()