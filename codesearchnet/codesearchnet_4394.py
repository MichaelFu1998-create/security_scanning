def clean_pair(cls, attribute, value):
    '''
    This will call `clean_attribute` on the attribute and also allows for the
    creation of boolean attributes.

    Ex. input(selected=True) is equivalent to input(selected="selected")
    '''
    attribute = cls.clean_attribute(attribute)

    # Check for boolean attributes
    # (i.e. selected=True becomes selected="selected")
    if value is True:
      value = attribute

    if value is False:
      value = "false"

    return (attribute, value)