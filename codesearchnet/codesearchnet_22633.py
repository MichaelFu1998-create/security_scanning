def get_doc(doc_id, db_name, server_url='http://127.0.0.1:5984/', rev=None):
    """Return a CouchDB document, given its ID, revision and database name."""
    db = get_server(server_url)[db_name]
    if rev:
        headers, response = db.resource.get(doc_id, rev=rev)
        return couchdb.client.Document(response)
    return db[doc_id]