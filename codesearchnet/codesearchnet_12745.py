def permission_check(data, command_permissions,
                     command=None, permissions=None):
    """
        Check the permissions of the user requesting a command

    Parameters
    ----------
    data : dict
        message data
    command_permissions : dict
        permissions of the command, contains all the roles as key and users
        with these permissions as values
    command : function
        the command that is run
    permissions : tuple or list
        a list of permissions for the command

    Returns
    -------
    bool
        True if the user has the right permissions, False otherwise
    """
    if permissions:
        pass
    elif command:
        if hasattr(command, 'permissions'):
            permissions = command.permissions
        else:
            return True  # true if no permission is required
    else:
        msg = "{name} must be called with command or permissions argument"
        raise RuntimeError(msg.format(name="_permission_check"))

    return any(data['sender']['id'] in command_permissions[permission]
               for permission in permissions
               if permission in command_permissions)