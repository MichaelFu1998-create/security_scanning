def prefetch_users(persistent_course_grades):
        """
        Prefetch Users from the list of user_ids present in the persistent_course_grades.

        Arguments:
            persistent_course_grades (list): A list of PersistentCourseGrade.

        Returns:
            (dict): A dictionary containing user_id to user mapping.
        """
        users = User.objects.filter(
            id__in=[grade.user_id for grade in persistent_course_grades]
        )
        return {
            user.id: user for user in users
        }