def get_reference_data(
            self,
            modified_since: Optional[datetime.datetime] = None
    ) -> GetReferenceDataResponse:
        """
        Fetches API reference data.

        :param modified_since: The response will be empty if no
        changes have been made to the reference data since this
        timestamp, otherwise all reference data will be returned.
        """

        if modified_since is None:
            modified_since = datetime.datetime(year=2010, month=1, day=1)

        response = requests.get(
            '{}/lovs'.format(API_URL_BASE),
            headers={
                'if-modified-since': self._format_dt(modified_since),
                **self._get_headers(),
            },
            timeout=self._timeout,
        )

        if not response.ok:
            raise FuelCheckError.create(response)

        # return response.text
        return GetReferenceDataResponse.deserialize(response.json())