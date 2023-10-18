def courses(self, request, enterprise_customer, pk=None):  # pylint: disable=invalid-name
        """
        Retrieve the list of courses contained within this catalog.

        Only courses with active course runs are returned. A course run is considered active if it is currently
        open for enrollment, or will open in the future.
        """
        catalog_api = CourseCatalogApiClient(request.user, enterprise_customer.site)
        courses = catalog_api.get_paginated_catalog_courses(pk, request.GET)

        # If the API returned an empty response, that means pagination has ended.
        # An empty response can also mean that there was a problem fetching data from catalog API.
        self.ensure_data_exists(
            request,
            courses,
            error_message=(
                "Unable to fetch API response for catalog courses from endpoint '{endpoint}'. "
                "The resource you are looking for does not exist.".format(endpoint=request.get_full_path())
            )
        )
        serializer = serializers.EnterpriseCatalogCoursesReadOnlySerializer(courses)

        # Add enterprise related context for the courses.
        serializer.update_enterprise_courses(enterprise_customer, catalog_id=pk)
        return get_paginated_response(serializer.data, request)