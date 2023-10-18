def compare(self, jwt: 'Jwt', compare_dates: bool = False) -> bool:
        """
        Compare against another `Jwt`.

        :param jwt: The token to compare against.
        :type jwt: Jwt
        :param compare_dates: Should the comparision take dates into account?
        :type compare_dates: bool
        :return: Are the two Jwt's the same?
        :rtype: bool
        """
        if self.secret != jwt.secret:
            return False
        if self.payload != jwt.payload:
            return False
        if self.alg != jwt.alg:
            return False
        if self.header != jwt.header:
            return False
        expected_claims = self.registered_claims
        actual_claims = jwt.registered_claims
        if not compare_dates:
            strip = ['exp', 'nbf', 'iat']
            expected_claims = {k: {v if k not in strip else None} for k, v in
                               expected_claims.items()}
            actual_claims = {k: {v if k not in strip else None} for k, v in
                             actual_claims.items()}
        if expected_claims != actual_claims:
            return False
        return True