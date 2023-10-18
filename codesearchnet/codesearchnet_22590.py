def log(self, string):
        """Log an event on the CouchDB server."""
        self.wfile.write(json.dumps({'log': string}) + NEWLINE)