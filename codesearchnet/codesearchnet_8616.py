def update_enterprise_courses(self, enterprise_customer, course_container_key='results', **kwargs):
        """
        This method adds enterprise-specific metadata for each course.

        We are adding following field in all the courses.
            tpa_hint: a string for identifying Identity Provider.
            enterprise_id: the UUID of the enterprise
            **kwargs: any additional data one would like to add on a per-use basis.

        Arguments:
            enterprise_customer: The customer whose data will be used to fill the enterprise context.
            course_container_key: The key used to find the container for courses in the serializer's data dictionary.
        """
        enterprise_context = {
            'tpa_hint': enterprise_customer and enterprise_customer.identity_provider,
            'enterprise_id': enterprise_customer and str(enterprise_customer.uuid),
        }
        enterprise_context.update(**kwargs)

        courses = []
        for course in self.data[course_container_key]:
            courses.append(
                self.update_course(course, enterprise_customer, enterprise_context)
            )
        self.data[course_container_key] = courses