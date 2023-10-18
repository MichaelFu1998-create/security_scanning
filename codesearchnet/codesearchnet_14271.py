def get_attribute(element, attribute, default=0):
    
    """ Returns XML element's attribute, or default if none.
    """ 
    
    a = element.getAttribute(attribute)
    if a == "": 
        return default
    return a