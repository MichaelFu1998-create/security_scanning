def _make_all_matchers(cls, parameters):
        '''
        For every parameter, create a matcher if the parameter has an
        annotation.
        '''
        for name, param in parameters:
            annotation = param.annotation
            if annotation is not Parameter.empty:
                yield name, cls._make_param_matcher(annotation, param.kind)