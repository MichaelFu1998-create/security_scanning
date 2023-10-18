def event_all_comments_list(request, slug):
    """
    Returns a list view of all comments for a given event.
    Combines event comments and update comments in one list.
    """
    event = get_object_or_404(Event, slug=slug)
    comments = event.all_comments
    page = int(request.GET.get('page', 99999))  # feed empty page by default to push to last page
    is_paginated = False
    if comments:
        paginator = Paginator(comments, 50)  # Show 50 comments per page
        try:
            comments = paginator.page(page)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            comments = paginator.page(paginator.num_pages)
        is_paginated = comments.has_other_pages()

    return render(request, 'happenings/event_comments.html', {
        "event": event,
        "comment_list": comments,
        "object_list": comments,
        "page_obj": comments,
        "page": page,
        "is_paginated": is_paginated,
        "key": key
    })