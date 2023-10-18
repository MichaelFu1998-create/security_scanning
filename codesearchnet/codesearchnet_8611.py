def transmit(self, payload, **kwargs):
        """
        Send a completion status call to SAP SuccessFactors using the client.

        Args:
            payload: The learner completion data payload to send to SAP SuccessFactors
        """
        kwargs['app_label'] = 'sap_success_factors'
        kwargs['model_name'] = 'SapSuccessFactorsLearnerDataTransmissionAudit'
        kwargs['remote_user_id'] = 'sapsf_user_id'
        super(SapSuccessFactorsLearnerTransmitter, self).transmit(payload, **kwargs)