def create_ical(request, slug):
    """ Creates an ical .ics file for an event using python-card-me. """
    event = get_object_or_404(Event, slug=slug)
    # convert dates to datetimes.
    # when we change code to datetimes, we won't have to do this.
    start = event.start_date
    start = datetime.datetime(start.year, start.month, start.day)

    if event.end_date:
        end = event.end_date
        end = datetime.datetime(end.year, end.month, end.day)
    else:
        end = start

    cal = card_me.iCalendar()
    cal.add('method').value = 'PUBLISH'
    vevent = cal.add('vevent')
    vevent.add('dtstart').value = start
    vevent.add('dtend').value = end
    vevent.add('dtstamp').value = datetime.datetime.now()
    vevent.add('summary').value = event.name
    response = HttpResponse(cal.serialize(), content_type='text/calendar')
    response['Filename'] = 'filename.ics'
    response['Content-Disposition'] = 'attachment; filename=filename.ics'
    return response