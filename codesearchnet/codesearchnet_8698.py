def paginated_list(object_list, page, page_size=25):
    """
    Returns paginated list.

    Arguments:
        object_list (QuerySet): A list of records to be paginated.
        page (int): Current page number.
        page_size (int): Number of records displayed in each paginated set.
        show_all (bool): Whether to show all records.

    Adopted from django/contrib/admin/templatetags/admin_list.py
    https://github.com/django/django/blob/1.11.1/django/contrib/admin/templatetags/admin_list.py#L50
    """
    paginator = CustomPaginator(object_list, page_size)
    try:
        object_list = paginator.page(page)
    except PageNotAnInteger:
        object_list = paginator.page(1)
    except EmptyPage:
        object_list = paginator.page(paginator.num_pages)

    page_range = []
    page_num = object_list.number

    # If there are 10 or fewer pages, display links to every page.
    # Otherwise, do some fancy
    if paginator.num_pages <= 10:
        page_range = range(paginator.num_pages)
    else:
        # Insert "smart" pagination links, so that there are always ON_ENDS
        # links at either end of the list of pages, and there are always
        # ON_EACH_SIDE links at either end of the "current page" link.
        if page_num > (PAGES_ON_EACH_SIDE + PAGES_ON_ENDS + 1):
            page_range.extend(range(1, PAGES_ON_ENDS + 1))
            page_range.append(DOT)
            page_range.extend(range(page_num - PAGES_ON_EACH_SIDE, page_num + 1))
        else:
            page_range.extend(range(1, page_num + 1))
        if page_num < (paginator.num_pages - PAGES_ON_EACH_SIDE - PAGES_ON_ENDS):
            page_range.extend(range(page_num + 1, page_num + PAGES_ON_EACH_SIDE + 1))
            page_range.append(DOT)
            page_range.extend(range(paginator.num_pages + 1 - PAGES_ON_ENDS, paginator.num_pages + 1))
        else:
            page_range.extend(range(page_num + 1, paginator.num_pages + 1))

        # Override page range to implement custom smart links.
        object_list.paginator.page_range = page_range

    return object_list