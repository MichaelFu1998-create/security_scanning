def add_event(request):
    """ Public form to add an event. """
    form = AddEventForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.sites = settings.SITE_ID
        instance.submitted_by = request.user
        instance.approved = True
        instance.slug = slugify(instance.name)
        instance.save()
        messages.success(request, 'Your event has been added.')
        return HttpResponseRedirect(reverse('events_index'))
    return render(request, 'happenings/event_form.html', {
        'form': form,
        'form_title': 'Add an event'
    })