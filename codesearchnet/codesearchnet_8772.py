def transmit(self, payload, **kwargs):
        """
        Send a completion status call to the integrated channel using the client.

        Args:
            payload: The learner completion data payload to send to the integrated channel.
            kwargs: Contains integrated channel-specific information for customized transmission variables.
                - app_label: The app label of the integrated channel for whom to store learner data records for.
                - model_name: The name of the specific learner data record model to use.
                - remote_user_id: The remote ID field name of the learner on the audit model.
        """
        IntegratedChannelLearnerDataTransmissionAudit = apps.get_model(  # pylint: disable=invalid-name
            app_label=kwargs.get('app_label', 'integrated_channel'),
            model_name=kwargs.get('model_name', 'LearnerDataTransmissionAudit'),
        )
        # Since we have started sending courses to integrated channels instead of course runs,
        # we need to attempt to send transmissions with course keys and course run ids in order to
        # ensure that we account for whether courses or course runs exist in the integrated channel.
        # The exporters have been changed to return multiple transmission records to attempt,
        # one by course key and one by course run id.
        # If the transmission with the course key succeeds, the next one will get skipped.
        # If it fails, the one with the course run id will be attempted and (presumably) succeed.
        for learner_data in payload.export():
            serialized_payload = learner_data.serialize(enterprise_configuration=self.enterprise_configuration)
            LOGGER.debug('Attempting to transmit serialized payload: %s', serialized_payload)

            enterprise_enrollment_id = learner_data.enterprise_course_enrollment_id
            if learner_data.completed_timestamp is None:
                # The user has not completed the course, so we shouldn't send a completion status call
                LOGGER.info('Skipping in-progress enterprise enrollment {}'.format(enterprise_enrollment_id))
                continue

            previous_transmissions = IntegratedChannelLearnerDataTransmissionAudit.objects.filter(
                enterprise_course_enrollment_id=enterprise_enrollment_id,
                error_message=''
            )
            if previous_transmissions.exists():
                # We've already sent a completion status call for this enrollment
                LOGGER.info('Skipping previously sent enterprise enrollment {}'.format(enterprise_enrollment_id))
                continue

            try:
                code, body = self.client.create_course_completion(
                    getattr(learner_data, kwargs.get('remote_user_id')),
                    serialized_payload
                )
                LOGGER.info(
                    'Successfully sent completion status call for enterprise enrollment {}'.format(
                        enterprise_enrollment_id,
                    )
                )
            except RequestException as request_exception:
                code = 500
                body = str(request_exception)
                self.handle_transmission_error(learner_data, request_exception)

            learner_data.status = str(code)
            learner_data.error_message = body if code >= 400 else ''
            learner_data.save()