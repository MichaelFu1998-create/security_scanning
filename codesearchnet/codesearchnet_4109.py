def _get_rules(self, cls):
        """Returns a list of rules of a given class
        
        Rules are treated as singletons - we only instantiate each
        rule once. 
        """

        result = []
        for rule_class in cls.__subclasses__():
            rule_name = rule_class.__name__.lower()
            if rule_name not in self._rules:
                rule = rule_class(self)
                self._rules[rule_name] = rule
            result.append(self._rules[rule_name])
        return result