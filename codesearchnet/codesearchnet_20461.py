def build(self):
        """
        Generates the policy document based on the internal lists of
        allowed and denied conditions. This will generate a policy with
        two main statements for the effect: one statement for Allow and
        one statement for Deny. Methods that includes conditions will
        have their own statement in the policy.
        """
        if ((self.allowMethods is None or len(self.allowMethods) == 0) and
                (self.denyMethods is None or len(self.denyMethods) == 0)):
            raise NameError('No statements defined for the policy')

        policy = {
            'principalId': self.principal_id,
            'policyDocument': {
                'Version': self.version,
                'Statement': []
            }
        }

        policy['policyDocument']['Statement'].extend(
            self._get_effect_statement('Allow', self.allowMethods))
        policy['policyDocument']['Statement'].extend(
            self._get_effect_statement('Deny', self.denyMethods))

        return policy