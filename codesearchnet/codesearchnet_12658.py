def without_tz(request):
    """
    Get the time without TZ enabled

    """
    
    t = Template('{% load tz %}{% get_current_timezone as TIME_ZONE %}{{ TIME_ZONE }}') 
    c = RequestContext(request)
    response = t.render(c)
    return HttpResponse(response)