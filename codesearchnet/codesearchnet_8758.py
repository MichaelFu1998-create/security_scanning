def transmit(self, payload, **kwargs):
        """
        Send a completion status call to Degreed using the client.

        Args:
            payload: The learner completion data payload to send to Degreed
        """
        kwargs['app_label'] = 'degreed'
        kwargs['model_name'] = 'DegreedLearnerDataTransmissionAudit'
        kwargs['remote_user_id'] = 'degreed_user_email'
        super(DegreedLearnerTransmitter, self).transmit(payload, **kwargs)