def spec_formatter(cls, spec):
        " Formats the elements of an argument set appropriately"
        return type(spec)((k, str(v)) for (k,v) in spec.items())