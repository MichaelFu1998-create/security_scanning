def is_threat(self, result=None, harmless_age=None, threat_score=None, threat_type=None):
        """
        Check if IP is a threat

        :param result: httpBL results; if None, then results from last check_ip() used (optional)
        :param harmless_age: harmless age for check if httpBL age is older (optional)
        :param threat_score: threat score for check if httpBL threat is lower (optional)
        :param threat_type:  threat type, if not equal httpBL score type, then return False (optional)
        :return: True or False
        """

        harmless_age = harmless_age if harmless_age is not None else settings.CACHED_HTTPBL_HARMLESS_AGE
        threat_score = threat_score if threat_score is not None else settings.CACHED_HTTPBL_THREAT_SCORE
        threat_type = threat_type if threat_type is not None else -1
        result = result if result is not None else self._last_result
        threat = False
        if result is not None:
            if result['age'] < harmless_age and result['threat'] > threat_score:
                threat = True
            if threat_type > -1:
                if result['type'] & threat_type:
                    threat = True
                else:
                    threat = False
        return threat