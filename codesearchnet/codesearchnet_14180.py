def is_math(str):
    
    """ Determines if an item in a paragraph is a LaTeX math equation.
    
    Math equations are wrapped in <math></math> tags.
    They can be drawn as an image using draw_math().
    
    """
    
    str = str.strip()
    if str.startswith("<math>") and str.endswith("</math>"):
        return True
    else:
        return False