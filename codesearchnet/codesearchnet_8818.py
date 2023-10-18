def commit(self):
        """
        Commit a real ``DataSharingConsent`` object to the database, mirroring current field settings.

        :return: A ``DataSharingConsent`` object if validation is successful, otherwise ``None``.
        """
        if self._child_consents:
            consents = []

            for consent in self._child_consents:
                consent.granted = self.granted
                consents.append(consent.save() or consent)

            return ProxyDataSharingConsent.from_children(self.program_uuid, *consents)

        consent, _ = DataSharingConsent.objects.update_or_create(
            enterprise_customer=self.enterprise_customer,
            username=self.username,
            course_id=self.course_id,
            defaults={
                'granted': self.granted
            }
        )
        self._exists = consent.exists
        return consent