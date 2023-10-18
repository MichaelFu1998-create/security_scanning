def with_tz(request):
    """
    Get the time with TZ enabled

    """
    
    dt = datetime.now() 
    t = Template('{% load tz %}{% localtime on %}{% get_current_timezone as TIME_ZONE %}{{ TIME_ZONE }}{% endlocaltime %}') 
    c = RequestContext(request)
    response = t.render(c)
    return HttpResponse(response)