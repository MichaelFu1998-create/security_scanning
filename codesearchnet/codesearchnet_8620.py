def get_learner_data_records(self, enterprise_enrollment, completed_date=None, grade=None, is_passing=False):
        """
        Generate a learner data transmission audit with fields properly filled in.
        """
        # pylint: disable=invalid-name
        LearnerDataTransmissionAudit = apps.get_model('integrated_channel', 'LearnerDataTransmissionAudit')
        completed_timestamp = None
        course_completed = False
        if completed_date is not None:
            completed_timestamp = parse_datetime_to_epoch_millis(completed_date)
            course_completed = is_passing

        return [
            LearnerDataTransmissionAudit(
                enterprise_course_enrollment_id=enterprise_enrollment.id,
                course_id=enterprise_enrollment.course_id,
                course_completed=course_completed,
                completed_timestamp=completed_timestamp,
                grade=grade,
            )
        ]