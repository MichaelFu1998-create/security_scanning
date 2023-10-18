def is_revision_publication(publication_id, cursor):
    """Checks to see if the publication contains any revised models.
    Revised in this context means that it is a new version of an
    existing piece of content.
    """
    cursor.execute("""\
SELECT 't'::boolean FROM modules
WHERE uuid IN (SELECT uuid
               FROM pending_documents
               WHERE publication_id = %s)
LIMIT 1""", (publication_id,))
    try:
        cursor.fetchone()[0]
    except TypeError:  # NoneType
        has_revision_models = False
    else:
        has_revision_models = True
    return has_revision_models