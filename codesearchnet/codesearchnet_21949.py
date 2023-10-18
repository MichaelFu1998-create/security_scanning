def get_upcoming_events(num, days, featured=False):
    """
    Get upcoming events.
    Allows slicing to a given number,
    picking the number of days to hold them after they've started
    and whether they should be featured or not.
    Usage:
    {% get_upcoming_events 5 14 featured as events %}
    Would return no more than 5 Featured events,
    holding them for 14 days past their start date.

    """
    from happenings.models import Event
    start_date = today - datetime.timedelta(days=days)
    events = Event.objects.filter(start_date__gt=start_date).order_by('start_date')
    if featured:
        events = events.filter(featured=True)
    events = events[:num]
    return events