def get_inactive_sap_learners(self):
        """
        Make a GET request using the session object to a SuccessFactors endpoint for inactive learners.

        Example:
            sap_search_student_url: "/learning/odatav4/searchStudent/v1/Students?
                $filter=criteria/isActive eq False&$select=studentID"

            SAP API response: {
                u'@odata.metadataEtag': u'W/"17090d86-20fa-49c8-8de0-de1d308c8b55"',
                u'value': [
                    {
                        u'studentID': u'admint6',
                    },
                    {
                        u'studentID': u'adminsap1',
                    }
                ]
            }

        Returns: List of inactive learners
        [
            {
                u'studentID': u'admint6'
            },
            {
                u'studentID': u'adminsap1'
            }
        ]
        """
        now = datetime.datetime.utcnow()
        if now >= self.expires_at:
            # Create a new session with a valid token
            self.session.close()
            self._create_session()

        sap_search_student_url = '{sapsf_base_url}/{search_students_path}?$filter={search_filter}'.format(
            sapsf_base_url=self.enterprise_configuration.sapsf_base_url.rstrip('/'),
            search_students_path=self.global_sap_config.search_student_api_path.rstrip('/'),
            search_filter='criteria/isActive eq False&$select=studentID',
        )
        all_inactive_learners = self._call_search_students_recursively(
            sap_search_student_url,
            all_inactive_learners=[],
            page_size=500,
            start_at=0
        )
        return all_inactive_learners