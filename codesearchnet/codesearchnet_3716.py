def _disassoc(self, url_fragment, me, other):
        """Disassociate the `other` record from the `me` record."""

        # Get the endpoint for foreign records within this object.
        url = self.endpoint + '%d/%s/' % (me, url_fragment)

        # Attempt to determine whether the other record already is absent, for the "changed" moniker.
        r = client.get(url, params={'id': other}).json()
        if r['count'] == 0:
            return {'changed': False}

        # Send a request removing the foreign record from this one.
        r = client.post(url, data={'disassociate': True, 'id': other})
        return {'changed': True}