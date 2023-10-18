def _fetch_course_enrollment_data(self, enterprise_customer_uuid):
        """
        Return enterprise customer UUID/user_id/course_run_id triples which represent CourseEnrollment records
        which do not have a matching EnterpriseCourseEnrollment record.

        The query used below looks for CourseEnrollment records that are associated with enterprise
        learners where the enrollment data is after the creation of the link between the learner
        and the enterprise. It also excludes learners with edx.org email addresses in order to
        filter out test users.
        """
        query = '''
            SELECT
                au.id as user_id,
                ecu.enterprise_customer_id as enterprise_customer_uuid,
                sce.course_id as course_run_id
            FROM student_courseenrollment sce
            JOIN auth_user au
                ON au.id = sce.user_id
            JOIN enterprise_enterprisecustomeruser ecu
                ON ecu.user_id = au.id
            LEFT JOIN enterprise_enterprisecourseenrollment ece
                ON ece.enterprise_customer_user_id = ecu.id
                AND ece.course_id = sce.course_id
            WHERE
                ece.id IS NULL
                AND ecu.created <= sce.created
                AND au.email NOT LIKE '%@edx.org'
                {enterprise_customer_filter}
            ORDER BY sce.created;
        '''

        with connection.cursor() as cursor:
            if enterprise_customer_uuid:
                cursor.execute(
                    query.format(enterprise_customer_filter='AND ecu.enterprise_customer_id = %s'),
                    [enterprise_customer_uuid]
                )
            else:
                cursor.execute(
                    query.format(enterprise_customer_filter='')
                )

            return self._dictfetchall(cursor)