def logrotate(filename):
    
    """
    Return the next available filename for a particular filename prefix.
    
    For example:
    
        >>> import os
        # Make three (empty) files in a directory
        >>> fp0 = open('file.0', 'w')
        >>> fp1 = open('file.1', 'w')
        >>> fp2 = open('file.2', 'w')
        >>> fp0.close(), fp1.close(), fp2.close()
        (None, None, None)
        # Use logrotate to get the next available filename.
        >>> logrotate('file')
        'file.3'
        >>> logrotate('file.2')
        'file.3'
        >>> logrotate('file.1')
        'file.3'
    
    This can be used to get the next available filename for logging, allowing
    you to rotate log files, without using Python's ``logging`` module.
    """

    match = re.match(r'(.*)' + re.escape(os.path.extsep) + r'(\d+)', filename)
    if os.path.exists(filename):
        if match:
            prefix, number = match.groups()
            number = int(number)
            while os.path.exists(os.path.extsep.join((prefix, str(number)))):
                number += 1
            return os.path.extsep.join((prefix, str(number)))
    elif match:
        return filename
    return logrotate(os.path.extsep.join((filename, '0')))