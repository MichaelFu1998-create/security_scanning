def post_accept_license(request):
    """Allows the user (at ``uid``) to accept the license(s) for
    a publication (at ``id``).
    """
    publication_id = request.matchdict['id']
    uid = request.matchdict['uid']

    # TODO Verify the accepting user is the one making the request.
    #      They could be authenticated but not be the license acceptor.

    post_data = request.json
    accepted = []
    denied = []
    try:
        documents = post_data['documents']
        for doc_acceptance in documents:
            if doc_acceptance['is_accepted'] is None:
                continue
            elif doc_acceptance['is_accepted']:
                accepted.append(doc_acceptance['id'])
            else:
                denied.append(doc_acceptance['id'])
    except KeyError:
        raise httpexceptions.BadRequest("Posted data is invalid.")

    # For each pending document, accept/deny the license.
    with db_connect() as db_conn:
        with db_conn.cursor() as cursor:
            accept_publication_license(cursor, publication_id, uid,
                                       accepted, True)
            accept_publication_license(cursor, publication_id, uid,
                                       denied, False)

    location = request.route_url('publication-license-acceptance',
                                 id=publication_id, uid=uid)
    # Poke publication to change state.
    poke_publication_state(publication_id)
    return httpexceptions.HTTPFound(location=location)