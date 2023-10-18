def _get_scopes(self):
        """Returns the scopes associated with this object, kept up to
         date for incremental auth."""
        if _credentials_from_request(self.request):
            return (self._scopes |
                    _credentials_from_request(self.request).scopes)
        else:
            return self._scopes