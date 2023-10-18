def add_memory(request, slug):
    """ Adds a memory to an event. """
    event = get_object_or_404(Event, slug=slug)
    form = MemoryForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.event = event
        instance.save()
        msg = "Your thoughts were added. "

        if request.FILES:
            photo_list = request.FILES.getlist('photos')
            photo_count = len(photo_list)
            for upload_file in photo_list:
                process_upload(upload_file, instance, form, event, request)
            if photo_count > 1:
                msg += "{} images were added and should appear soon.".format(photo_count)
            else:
                msg += "{} image was added and should appear soon.".format(photo_count)
        messages.success(request, msg)
        return HttpResponseRedirect('../')
    return render(request, 'happenings/add_memories.html', {'form': form, 'event': event})