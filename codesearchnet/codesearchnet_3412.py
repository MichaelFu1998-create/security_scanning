def binary_arch(binary):
    """
    helper method for determining binary architecture

    :param binary: str for binary to introspect.
    :rtype bool: True for x86_64, False otherwise
    """

    with open(binary, 'rb') as f:
        elffile = ELFFile(f)
        if elffile['e_machine'] == 'EM_X86_64':
            return True
        else:
            return False