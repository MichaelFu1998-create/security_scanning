def event_update_list(request, slug):
    """
    Returns a list view of updates for a given event.
    If the event is over, it will be in chronological order.
    If the event is upcoming or still going,
    it will be in reverse chronological order.
    """
    event = get_object_or_404(Event, slug=slug)
    updates = Update.objects.filter(event__slug=slug)
    if event.recently_ended():
        # if the event is over, use chronological order
        updates = updates.order_by('id')
    else:
        # if not, use reverse chronological
        updates = updates.order_by('-id')
    return render(request, 'happenings/updates/update_list.html', {
        'event': event,
        'object_list': updates,
    })