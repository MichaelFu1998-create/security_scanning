def video_list(request, slug):
    """
    Displays list of videos for given event.
    """
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'video/video_list.html', {
        'event': event,
        'video_list': event.eventvideo_set.all()
    })