def get_content_metadata(self, enterprise_customer):
        """
        Return all content metadata contained in the catalogs associated with the EnterpriseCustomer.

        Arguments:
            enterprise_customer (EnterpriseCustomer): The EnterpriseCustomer to return content metadata for.

        Returns:
            list: List of dicts containing content metadata.
        """
        content_metadata = OrderedDict()

        # TODO: This if block can be removed when we get rid of discovery service-based catalogs.
        if enterprise_customer.catalog:
            response = self._load_data(
                self.ENTERPRISE_CUSTOMER_ENDPOINT,
                detail_resource='courses',
                resource_id=str(enterprise_customer.uuid),
                traverse_pagination=True,
            )
            for course in response['results']:
                for course_run in course['course_runs']:
                    course_run['content_type'] = 'courserun'  # Make this look like a search endpoint result.
                    content_metadata[course_run['key']] = course_run

        for enterprise_customer_catalog in enterprise_customer.enterprise_customer_catalogs.all():
            response = self._load_data(
                self.ENTERPRISE_CUSTOMER_CATALOGS_ENDPOINT,
                resource_id=str(enterprise_customer_catalog.uuid),
                traverse_pagination=True,
                querystring={'page_size': 1000},
            )

            for item in response['results']:
                content_id = utils.get_content_metadata_item_id(item)
                content_metadata[content_id] = item

        return content_metadata.values()