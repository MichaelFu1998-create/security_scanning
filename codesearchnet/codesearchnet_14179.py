def is_list(str):
 
    """ Determines if an item in a paragraph is a list.

    If all of the lines in the markup start with a "*" or "1." 
    this indicates a list as parsed by parse_paragraphs().
    It can be drawn with draw_list().
    
    """ 
    
    for chunk in str.split("\n"):
        chunk = chunk.replace("\t", "")
        if  not chunk.lstrip().startswith("*") \
        and not re.search(r"^([0-9]{1,3}\. )", chunk.lstrip()):
            return False
    
    return True