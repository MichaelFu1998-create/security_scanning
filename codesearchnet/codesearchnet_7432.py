def _validate(self, conditions):
        """ Validate saved search conditions, raising an error if any contain invalid operators """
        allowed_keys = set(self.searchkeys)
        operators_set = set(self.operators.keys())
        for condition in conditions:
            if set(condition.keys()) != allowed_keys:
                raise ze.ParamNotPassed(
                    "Keys must be all of: %s" % ", ".join(self.searchkeys)
                )
            if condition.get("operator") not in operators_set:
                raise ze.ParamNotPassed(
                    "You have specified an unknown operator: %s"
                    % condition.get("operator")
                )
            # dict keys of allowed operators for the current condition
            permitted_operators = self.conditions_operators.get(
                condition.get("condition")
            )
            # transform these into values
            permitted_operators_list = set(
                [self.operators.get(op) for op in permitted_operators]
            )
            if condition.get("operator") not in permitted_operators_list:
                raise ze.ParamNotPassed(
                    "You may not use the '%s' operator when selecting the '%s' condition. \nAllowed operators: %s"
                    % (
                        condition.get("operator"),
                        condition.get("condition"),
                        ", ".join(list(permitted_operators_list)),
                    )
                )