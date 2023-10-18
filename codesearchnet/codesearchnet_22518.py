def djeffify_string(string_to_djeff):
    """
    Djeffifies string_to_djeff
    """
    string_to_djeff = re.sub(r'^(?=[jg])', 'd', string_to_djeff, flags=re.IGNORECASE)  # first
    string_to_djeff = re.sub(r'[ ](?=[jg])', ' d', string_to_djeff, flags=re.IGNORECASE)  # spaces
    string_to_djeff = re.sub(r'[\n](?=[jg])', '\nd', string_to_djeff, flags=re.IGNORECASE)  # \n
    return string_to_djeff