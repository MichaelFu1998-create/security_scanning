def mfa_otp_login(self, temp_token, one_time_pass):
        """
        Log in to get the real token using the temporary token and otp.

        :param temp_token: The temporary token or id returned from normal login
        :type temp_token: string
        :param one_time_pass: The one-time pass to be sent to the underlying
            multi-factor engine.
        :type one_time_pass: string
        :returns: A standard token for interacting with the web api.
        :rtype: string
        """
        parameters = dict()
        parameters['mfaTokenId'] = temp_token
        parameters['otp'] = one_time_pass
        response = self.request('midas.mfa.otp.login', parameters)
        return response['token']