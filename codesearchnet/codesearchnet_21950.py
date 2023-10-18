def get_events_by_date_range(days_out, days_hold, max_num=5, featured=False):
    """
    Get upcoming events for a given number of days (days out)
    Allows specifying number of days to hold events after they've started
    The max number to show (defaults to 5)
    and whether they should be featured or not.
    Usage:
    {% get_events_by_date_range 14 3 3 'featured' as events %}
    Would return no more than 3 featured events,
    that fall within the next 14 days or have ended within the past 3.
    """
    from happenings.models import Event
    range_start = today - datetime.timedelta(days=days_hold)
    range_end = today + datetime.timedelta(days=days_out)

    events = Event.objects.filter(
        start_date__gte=range_start,
        start_date__lte=range_end
    ).order_by('start_date')
    if featured:
        events = events.filter(featured=True)
    events = events[:max_num]
    return events