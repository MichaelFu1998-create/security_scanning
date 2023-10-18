def convert_permissions(m_perms):
    """
    Converts a Manticore permission string into a Unicorn permission
    :param m_perms: Manticore perm string ('rwx')
    :return: Unicorn Permissions
    """
    permissions = UC_PROT_NONE
    if 'r' in m_perms:
        permissions |= UC_PROT_READ
    if 'w' in m_perms:
        permissions |= UC_PROT_WRITE
    if 'x' in m_perms:
        permissions |= UC_PROT_EXEC
    return permissions