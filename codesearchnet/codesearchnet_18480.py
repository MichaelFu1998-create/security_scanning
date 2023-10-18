def _pop_claims_from_payload(self):
        """
        Check for registered claims in the payload and move them to the
        registered_claims property, overwriting any extant claims.
        """
        claims_in_payload = [k for k in self.payload.keys() if
                             k in registered_claims.values()]
        for name in claims_in_payload:
            self.registered_claims[name] = self.payload.pop(name)