def _find_descendents(self, url):
        """Return properties document for url and all children."""
        # Ad-hoc query for URL starting with a prefix
        map_fun = """function(doc) {
                var url = doc.url + "/";
                if(doc.type === 'properties' && url.indexOf('%s') === 0) {
                    emit(doc.url, { 'id': doc._id, 'url': doc.url });
                }
            }""" % (
            url + "/"
        )
        vr = self.db.query(map_fun, include_docs=True)
        for row in vr:
            yield row.doc
        return