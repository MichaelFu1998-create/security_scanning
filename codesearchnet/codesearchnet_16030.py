def validate_content(*objs):
    """Runs the correct validator for given `obj`ects. Assumes all same type"""
    from .main import Collection, Module
    validator = {
        Collection: cnxml.validate_collxml,
        Module: cnxml.validate_cnxml,
    }[type(objs[0])]
    return validator(*[obj.file for obj in objs])