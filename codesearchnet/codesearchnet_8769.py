def _call_search_students_recursively(self, sap_search_student_url, all_inactive_learners, page_size, start_at):
        """
        Make recursive GET calls to traverse the paginated API response for search students.
        """
        search_student_paginated_url = '{sap_search_student_url}&{pagination_criterion}'.format(
            sap_search_student_url=sap_search_student_url,
            pagination_criterion='$count=true&$top={page_size}&$skip={start_at}'.format(
                page_size=page_size,
                start_at=start_at,
            ),
        )
        try:
            response = self.session.get(search_student_paginated_url)
            sap_inactive_learners = response.json()
        except (ConnectionError, Timeout):
            LOGGER.warning(
                'Unable to fetch inactive learners from SAP searchStudent API with url '
                '"{%s}".', search_student_paginated_url,
            )
            return None

        if 'error' in sap_inactive_learners:
            LOGGER.warning(
                'SAP searchStudent API for customer %s and base url %s returned response with '
                'error message "%s" and with error code "%s".',
                self.enterprise_configuration.enterprise_customer.name,
                self.enterprise_configuration.sapsf_base_url,
                sap_inactive_learners['error'].get('message'),
                sap_inactive_learners['error'].get('code'),
            )
            return None

        new_page_start_at = page_size + start_at
        all_inactive_learners += sap_inactive_learners['value']
        if sap_inactive_learners['@odata.count'] > new_page_start_at:
            return self._call_search_students_recursively(
                sap_search_student_url,
                all_inactive_learners,
                page_size=page_size,
                start_at=new_page_start_at,
            )

        return all_inactive_learners