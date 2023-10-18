def get_learner_data_records(
            self,
            enterprise_enrollment,
            completed_date=None,
            is_passing=False,
            **kwargs
    ):  # pylint: disable=arguments-differ,unused-argument
        """
        Return a DegreedLearnerDataTransmissionAudit with the given enrollment and course completion data.

        If completed_date is None, then course completion has not been met.

        If no remote ID can be found, return None.
        """
        # Degreed expects completion dates of the form 'yyyy-mm-dd'.
        completed_timestamp = completed_date.strftime("%F") if isinstance(completed_date, datetime) else None
        if enterprise_enrollment.enterprise_customer_user.get_remote_id() is not None:
            DegreedLearnerDataTransmissionAudit = apps.get_model(  # pylint: disable=invalid-name
                'degreed',
                'DegreedLearnerDataTransmissionAudit'
            )
            # We return two records here, one with the course key and one with the course run id, to account for
            # uncertainty about the type of content (course vs. course run) that was sent to the integrated channel.
            return [
                DegreedLearnerDataTransmissionAudit(
                    enterprise_course_enrollment_id=enterprise_enrollment.id,
                    degreed_user_email=enterprise_enrollment.enterprise_customer_user.user_email,
                    course_id=parse_course_key(enterprise_enrollment.course_id),
                    course_completed=completed_date is not None and is_passing,
                    completed_timestamp=completed_timestamp,
                ),
                DegreedLearnerDataTransmissionAudit(
                    enterprise_course_enrollment_id=enterprise_enrollment.id,
                    degreed_user_email=enterprise_enrollment.enterprise_customer_user.user_email,
                    course_id=enterprise_enrollment.course_id,
                    course_completed=completed_date is not None and is_passing,
                    completed_timestamp=completed_timestamp,
                )
            ]
        else:
            LOGGER.debug(
                'No learner data was sent for user [%s] because a Degreed user ID could not be found.',
                enterprise_enrollment.enterprise_customer_user.username
            )