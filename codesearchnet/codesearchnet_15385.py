def add_pending_model_content(cursor, publication_id, model):
    """Updates the pending model's content.
    This is a secondary step not in ``add_pending_model, because
    content reference resolution requires the identifiers as they
    will appear in the end publication.
    """
    cursor.execute("""\
        SELECT id, ident_hash(uuid, major_version, minor_version)
        FROM pending_documents
        WHERE publication_id = %s AND uuid = %s""",
                   (publication_id, model.id,))
    document_info = cursor.fetchone()

    def attach_info_to_exception(exc):
        """Small cached function to grab the pending document id
        and hash to attach to the exception, which is useful when
        reading the json data on a response.
        """
        exc.publication_id = publication_id
        exc.pending_document_id, exc.pending_ident_hash = document_info

    def mark_invalid_reference(reference):
        """Set the publication to failure and attach invalid reference
        to the publication.
        """
        exc = exceptions.InvalidReference(reference)
        attach_info_to_exception(exc)
        set_publication_failure(cursor, exc)

    for resource in getattr(model, 'resources', []):
        add_pending_resource(cursor, resource, document=model)

    if isinstance(model, cnxepub.Document):
        for reference in model.references:
            if reference.is_bound:
                reference.bind(reference.bound_model, '/resources/{}')
            elif reference.remote_type == cnxepub.INTERNAL_REFERENCE_TYPE:
                if reference.uri.startswith('#'):
                    pass
                elif reference.uri.startswith('/contents'):
                    ident_hash = parse_archive_uri(reference.uri)
                    try:
                        doc_pointer = lookup_document_pointer(
                            ident_hash, cursor)
                    except DocumentLookupError:
                        mark_invalid_reference(reference)
                    else:
                        reference.bind(doc_pointer, "/contents/{}")
                else:
                    mark_invalid_reference(reference)
            # else, it's a remote or cnx.org reference ...Do nothing.

        args = (psycopg2.Binary(model.content.encode('utf-8')),
                publication_id, model.id,)
        stmt = """\
            UPDATE "pending_documents"
            SET ("content") = (%s)
            WHERE "publication_id" = %s AND "uuid" = %s"""
    else:
        metadata = model.metadata.copy()
        # All document pointers in the tree are valid?
        document_pointers = [m for m in cnxepub.flatten_model(model)
                             if isinstance(m, cnxepub.DocumentPointer)]
        document_pointer_ident_hashes = [
            (split_ident_hash(dp.ident_hash)[0],
             split_ident_hash(dp.ident_hash, split_version=True)[1][0],
             split_ident_hash(dp.ident_hash, split_version=True)[1][1],)
            #  split_ident_hash(dp.ident_hash, split_version=True)[1][0],)
            for dp in document_pointers]
        document_pointer_ident_hashes = zip(*document_pointer_ident_hashes)

        if document_pointers:
            uuids, major_vers, minor_vers = document_pointer_ident_hashes
            cursor.execute("""\
SELECT dp.uuid, module_version(dp.maj_ver, dp.min_ver) AS version,
       dp.uuid = m.uuid AS exists,
       m.portal_type = 'Module' AS is_document
FROM (SELECT unnest(%s::uuid[]), unnest(%s::integer[]), unnest(%s::integer[]))\
         AS dp(uuid, maj_ver, min_ver)
     LEFT JOIN modules AS m ON dp.uuid = m.uuid AND \
         (dp.maj_ver = m.major_version OR dp.maj_ver is null)""",
                           (list(uuids), list(major_vers), list(minor_vers),))
            valid_pointer_results = cursor.fetchall()
            for result_row in valid_pointer_results:
                uuid, version, exists, is_document = result_row
                if not (exists and is_document):
                    dp = [dp for dp in document_pointers
                          if dp.ident_hash == join_ident_hash(uuid, version)
                          ][0]
                    exc = exceptions.InvalidDocumentPointer(
                        dp, exists=exists, is_document=is_document)
                    attach_info_to_exception(exc)
                    set_publication_failure(cursor, exc)

        # Insert the tree into the metadata.
        metadata['_tree'] = cnxepub.model_to_tree(model)
        args = (json.dumps(metadata),
                None,  # TODO Render the HTML tree at ``model.content``.
                publication_id, model.id,)
        # Must pave over metadata because postgresql lacks built-in
        # json update functions.
        stmt = """\
            UPDATE "pending_documents"
            SET ("metadata", "content") = (%s, %s)
            WHERE "publication_id" = %s AND "uuid" = %s"""
    cursor.execute(stmt, args)