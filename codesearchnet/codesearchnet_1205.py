def __manglePrivateMemberName(self, privateMemberName, skipCheck=False):
    """ Mangles the given mangled (private) member name; a mangled member name
    is one whose name begins with two or more underscores and ends with one
    or zero underscores.

    privateMemberName:
                  The private member name (e.g., "__logger")

    skipCheck:    Pass True to skip test for presence of the demangled member
                  in our instance.

    Returns:      The demangled member name (e.g., "_HTMPredictionModel__logger")
    """

    assert privateMemberName.startswith("__"), \
           "%r doesn't start with __" % privateMemberName
    assert not privateMemberName.startswith("___"), \
           "%r starts with ___" % privateMemberName
    assert not privateMemberName.endswith("__"), \
           "%r ends with more than one underscore" % privateMemberName

    realName = "_" + (self.__myClassName).lstrip("_") + privateMemberName

    if not skipCheck:
      # This will throw an exception if the member is missing
      getattr(self, realName)

    return realName