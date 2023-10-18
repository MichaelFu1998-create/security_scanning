def validate_course_run_id(self, value):
        """
        Validates that the course run id is part of the Enterprise Customer's catalog.
        """
        enterprise_customer = self.context.get('enterprise_customer')

        if not enterprise_customer.catalog_contains_course(value):
            raise serializers.ValidationError(
                'The course run id {course_run_id} is not in the catalog '
                'for Enterprise Customer {enterprise_customer}'.format(
                    course_run_id=value,
                    enterprise_customer=enterprise_customer.name,
                )
            )

        return value