def admin_obj_link(obj, display=''):
    """Returns a link to the django admin change list with a filter set to
    only the object given.

    :param obj:
        Object to create the admin change list display link for
    :param display:
        Text to display in the link.  Defaults to string call of the object
    :returns:
        Text containing HTML for a link
    """
    # get the url for the change list for this object
    url = reverse('admin:%s_%s_changelist' % (obj._meta.app_label,
        obj._meta.model_name))
    url += '?id__exact=%s' % obj.id

    text = str(obj)
    if display:
        text = display

    return format_html('<a href="{}">{}</a>', url, text)