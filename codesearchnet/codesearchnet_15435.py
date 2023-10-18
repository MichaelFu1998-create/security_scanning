def publish(request):
    """Accept a publication request at form value 'epub'"""
    if 'epub' not in request.POST:
        raise httpexceptions.HTTPBadRequest("Missing EPUB in POST body.")

    is_pre_publication = asbool(request.POST.get('pre-publication'))
    epub_upload = request.POST['epub'].file
    try:
        epub = cnxepub.EPUB.from_file(epub_upload)
    except:  # noqa: E722
        raise httpexceptions.HTTPBadRequest('Format not recognized.')

    # Make a publication entry in the database for status checking
    # the publication. This also creates publication entries for all
    # of the content in the EPUB.
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            epub_upload.seek(0)
            publication_id, publications = add_publication(
                cursor, epub, epub_upload, is_pre_publication)

    # Poke at the publication & lookup its state.
    state, messages = poke_publication_state(publication_id)

    response_data = {
        'publication': publication_id,
        'mapping': publications,
        'state': state,
        'messages': messages,
    }
    return response_data