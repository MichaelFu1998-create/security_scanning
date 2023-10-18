def is_user_enrolled(cls, user, course_id, course_mode):
        """
        Query the enrollment API and determine if a learner is enrolled in a given course run track.

        Args:
            user: The user whose enrollment needs to be checked
            course_mode: The mode with which the enrollment should be checked
            course_id: course id of the course where enrollment should be checked.

        Returns:
            Boolean: Whether or not enrollment exists

        """
        enrollment_client = EnrollmentApiClient()
        try:
            enrollments = enrollment_client.get_course_enrollment(user.username, course_id)
            if enrollments and course_mode == enrollments.get('mode'):
                return True
        except HttpClientError as exc:
            logging.error(
                'Error while checking enrollment status of user %(user)s: %(message)s',
                dict(user=user.username, message=str(exc))
            )
        except KeyError as exc:
            logging.warning(
                'Error while parsing enrollment data of user %(user)s: %(message)s',
                dict(user=user.username, message=str(exc))
            )
        return False