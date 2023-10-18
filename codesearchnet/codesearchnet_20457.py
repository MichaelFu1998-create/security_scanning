def _add_method(self, effect, verb, resource, conditions):
        """
        Adds a method to the internal lists of allowed or denied methods.
        Each object in the internal list contains a resource ARN and a
        condition statement. The condition statement can be null.
        """
        if verb != '*' and not hasattr(HttpVerb, verb):
            raise NameError('Invalid HTTP verb ' + verb +
                            '. Allowed verbs in HttpVerb class')
        resource_pattern = re.compile(self.path_regex)
        if not resource_pattern.match(resource):
            raise NameError('Invalid resource path: ' + resource +
                            '. Path should match ' + self.path_regex)

        if resource[:1] == '/':
            resource = resource[1:]

        resource_arn = ('arn:aws:execute-api:' +
                        self.region + ':' +
                        self.aws_account_id + ':' +
                        self.rest_api_id + '/' +
                        self.stage + '/' +
                        verb + '/' +
                        resource)

        if effect.lower() == 'allow':
            self.allowMethods.append({
                'resource_arn': resource_arn,
                'conditions': conditions
            })
        elif effect.lower() == 'deny':
            self.denyMethods.append({
                'resource_arn': resource_arn,
                'conditions': conditions
            })