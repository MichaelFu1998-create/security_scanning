def _get_effect_statement(self, effect, methods):
        """
        This function loops over an array of objects containing
        a resourceArn and conditions statement and generates
        the array of statements for the policy.
        """
        statements = []

        if len(methods) > 0:
            statement = self._get_empty_statement(effect)

            for method in methods:
                if (method['conditions'] is None or
                        len(method['conditions']) == 0):
                    statement['Resource'].append(method['resource_arn'])
                else:
                    cond_statement = self._get_empty_statement(effect)
                    cond_statement['Resource'].append(method['resource_arn'])
                    cond_statement['Condition'] = method['conditions']
                    statements.append(cond_statement)
            statements.append(statement)

        return statements