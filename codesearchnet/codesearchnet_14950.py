def get_or_create_shared_key(cls, force_new=False):
        """
        Create a shared public/private key pair for certificate pushing,
        if the settings allow.
        """
        if force_new:
            with transaction.atomic():
                SharedKey.objects.filter(current=True).update(current=False)
                key = Key()
                return SharedKey.objects.create(public_key=key,
                                                private_key=key,
                                                current=True)
        # create a new shared key if one doesn't exist
        try:
            return SharedKey.objects.get(current=True)
        except SharedKey.DoesNotExist:
            key = Key()
            return SharedKey.objects.create(public_key=key,
                                            private_key=key,
                                            current=True)