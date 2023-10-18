def _make_param_matcher(annotation, kind=None):
        '''
        For a given annotation, return a function which, when called on a
        function argument, returns true if that argument matches the annotation.
        If the annotation is a type, it calls isinstance; if it's a callable,
        it calls it on the object; otherwise, it performs a value comparison.
        If the parameter is variadic (*args) and the annotation is a type, the
        matcher will attempt to match each of the arguments in args
        '''
        if isinstance(annotation, type) or (
                isinstance(annotation, tuple) and
                all(isinstance(a, type) for a in annotation)):
            if kind is Parameter.VAR_POSITIONAL:
                return (lambda args: all(isinstance(x, annotation) for x in args))
            else:
                return (lambda x: isinstance(x, annotation))
        elif callable(annotation):
            return annotation
        else:
            return (lambda x: x == annotation)