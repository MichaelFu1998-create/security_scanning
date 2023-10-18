def retrieve(self, request, pk=None):  # pylint: disable=invalid-name
        """
        DRF view to get catalog details.

        Arguments:
            request (HttpRequest): Current request
            pk (int): Course catalog identifier

        Returns:
            (Response): DRF response object containing course catalogs.
        """
        catalog_api = CourseCatalogApiClient(request.user)
        catalog = catalog_api.get_catalog(pk)
        self.ensure_data_exists(
            request,
            catalog,
            error_message=(
                "Unable to fetch API response for given catalog from endpoint '/catalog/{pk}/'. "
                "The resource you are looking for does not exist.".format(pk=pk)
            )
        )
        serializer = self.serializer_class(catalog)
        return Response(serializer.data)