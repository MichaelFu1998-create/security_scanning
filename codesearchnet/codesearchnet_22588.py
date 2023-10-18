def handle_validate(self, function_name, new_doc, old_doc, user_ctx):
        """Validate...this function is undocumented, but still in CouchDB."""
        try:
            function = get_function(function_name)
        except Exception, exc:
            self.log(repr(exc))
            return False
        try:
            return function(new_doc, old_doc, user_ctx)
        except Exception, exc:
            self.log(repr(exc))
            return repr(exc)