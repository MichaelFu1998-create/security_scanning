def regenerate_signing_key(self, secret_key=None, region=None,
                               service=None, date=None):
        """
        Regenerate the signing key for this instance. Store the new key in
        signing_key property.

        Take scope elements of the new key from the equivalent properties
        (region, service, date) of the current AWS4Auth instance. Scope
        elements can be overridden for the new key by supplying arguments to
        this function. If overrides are supplied update the current AWS4Auth
        instance's equivalent properties to match the new values.

        If secret_key is not specified use the value of the secret_key property
        of the current AWS4Auth instance's signing key. If the existing signing
        key is not storing its secret key (i.e. store_secret_key was set to
        False at instantiation) then raise a NoSecretKeyError and do not
        regenerate the key. In order to regenerate a key which is not storing
        its secret key, secret_key must be supplied to this function.

        Use the value of the existing key's store_secret_key property when
        generating the new key. If there is no existing key, then default
        to setting store_secret_key to True for new key.

        """
        if secret_key is None and (self.signing_key is None or
                                   self.signing_key.secret_key is None):
            raise NoSecretKeyError

        secret_key = secret_key or self.signing_key.secret_key
        region = region or self.region
        service = service or self.service
        date = date or self.date
        if self.signing_key is None:
            store_secret_key = True
        else:
            store_secret_key = self.signing_key.store_secret_key

        self.signing_key = AWS4SigningKey(secret_key, region, service, date,
                                          store_secret_key)

        self.region = region
        self.service = service
        self.date = self.signing_key.date