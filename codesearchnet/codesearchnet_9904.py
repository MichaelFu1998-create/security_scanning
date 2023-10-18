def as_parameters(*parameters, variables=None):
        """
        Dump python list as the parameter of javascript function
        :param parameters:
        :param variables:
        :return:
        """
        s = json.dumps(parameters)
        s = s[1:-1]
        if variables:
            for v in variables:
                if v in parameters:
                    s = s.replace('"' + v + '"', v)
        return s