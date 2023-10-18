def get_course_completions(self, enterprise_customer, days):
        """
        Get course completions via PersistentCourseGrade for all the learners of given enterprise customer.

        Arguments:
            enterprise_customer (EnterpriseCustomer): Include Course enrollments for learners
                of this enterprise customer.
            days (int): Include course enrollment of this number of days.

        Returns:
            (list): A list of PersistentCourseGrade objects.
        """
        return PersistentCourseGrade.objects.filter(
            passed_timestamp__gt=datetime.datetime.now() - datetime.timedelta(days=days)
        ).filter(
            user_id__in=enterprise_customer.enterprise_customer_users.values_list('user_id', flat=True)
        )