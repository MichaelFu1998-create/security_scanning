def add_publication(cursor, epub, epub_file, is_pre_publication=False):
    """Adds a publication entry and makes each item
    a pending document.
    """
    publisher = epub[0].metadata['publisher']
    publish_message = epub[0].metadata['publication_message']
    epub_binary = psycopg2.Binary(epub_file.read())
    args = (publisher, publish_message, epub_binary, is_pre_publication,)
    cursor.execute("""\
INSERT INTO publications
  ("publisher", "publication_message", "epub", "is_pre_publication")
VALUES (%s, %s, %s, %s)
RETURNING id
""", args)
    publication_id = cursor.fetchone()[0]
    insert_mapping = {}

    models = set([])
    for package in epub:
        binder = cnxepub.adapt_package(package)
        if binder in models:
            continue
        for document in cnxepub.flatten_to_documents(binder):
            if document not in models:
                ident_hash = add_pending_model(
                    cursor, publication_id, document)
                insert_mapping[document.id] = ident_hash
                models.add(document)
        # The binding object could be translucent/see-through,
        # (case for a binder that only contains loose-documents).
        # Otherwise we should also publish the the binder.
        if not binder.is_translucent:
            ident_hash = add_pending_model(cursor, publication_id, binder)
            insert_mapping[binder.id] = ident_hash
            models.add(binder)
    for model in models:
        # Now that all models have been given an identifier
        # we can write the content to the database.
        try:
            add_pending_model_content(cursor, publication_id, model)
        except ResourceFileExceededLimitError as e:
            e.publication_id = publication_id
            set_publication_failure(cursor, e)
    return publication_id, insert_mapping