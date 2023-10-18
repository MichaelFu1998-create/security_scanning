def dropbox_submission(dropbox, request):
    """ handles the form submission, redirects to the dropbox's status page."""
    try:
        data = dropbox_schema.deserialize(request.POST)
    except Exception:
        return HTTPFound(location=request.route_url('dropbox_form'))

    # set the message
    dropbox.message = data.get('message')

    # recognize submission from watchdog
    if 'testing_secret' in dropbox.settings:
        dropbox.from_watchdog = is_equal(
            unicode(dropbox.settings['test_submission_secret']),
            data.pop('testing_secret', u''))

    # a non-js client might have uploaded an attachment via the form's fileupload field:
    if data.get('upload') is not None:
        dropbox.add_attachment(data['upload'])

    # now we can call the process method
    dropbox.submit()
    drop_url = request.route_url('dropbox_view', drop_id=dropbox.drop_id)
    print("Created dropbox %s" % drop_url)
    return HTTPFound(location=drop_url)