def paginate_update(update):
    """
    attempts to get next and previous on updates
    """
    from happenings.models import Update
    time = update.pub_time
    event = update.event
    try:
        next = Update.objects.filter(
            event=event,
            pub_time__gt=time
        ).order_by('pub_time').only('title')[0]
    except:
        next = None
    try:
        previous = Update.objects.filter(
            event=event,
            pub_time__lt=time
        ).order_by('-pub_time').only('title')[0]
    except:
        previous = None
    return {'next': next, 'previous': previous, 'event': event}