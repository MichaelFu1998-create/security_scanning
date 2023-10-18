def deny_method_with_conditions(self, verb, resource, conditions):
        """
        Adds an API Gateway method (Http verb + Resource path) to the
        list of denied methods and includes a condition for the policy
        statement. More on AWS policy conditions here:
        http://docs.aws.amazon.com/IAM/latest/UserGuide/
        reference_policies_elements.html#Condition
        """
        self._add_method('Deny', verb, resource, conditions)