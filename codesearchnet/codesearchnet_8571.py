def is_course_in_catalog(self, catalog_id, course_id):
        """
        Determine if the given course or course run ID is contained in the catalog with the given ID.

        Args:
            catalog_id (int): The ID of the catalog
            course_id (str): The ID of the course or course run

        Returns:
            bool: Whether the course or course run is contained in the given catalog
        """
        try:
            # Determine if we have a course run ID, rather than a plain course ID
            course_run_id = str(CourseKey.from_string(course_id))
        except InvalidKeyError:
            course_run_id = None

        endpoint = self.client.catalogs(catalog_id).contains

        if course_run_id:
            resp = endpoint.get(course_run_id=course_run_id)
        else:
            resp = endpoint.get(course_id=course_id)

        return resp.get('courses', {}).get(course_id, False)