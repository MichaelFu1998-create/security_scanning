def _get_doc_from_filename(filename):
    """Get SBMLDocument from given filename.

    Parameters
    ----------
    filename : path to SBML, or SBML string, or filehandle

    Returns
    -------
    libsbml.SBMLDocument
    """
    if isinstance(filename, string_types):
        if ("win" in platform) and (len(filename) < 260) \
                and os.path.exists(filename):
            # path (win)
            doc = libsbml.readSBMLFromFile(filename)  # noqa: E501 type: libsbml.SBMLDocument
        elif ("win" not in platform) and os.path.exists(filename):
            # path other
            doc = libsbml.readSBMLFromFile(filename)  # noqa: E501 type: libsbml.SBMLDocument
        else:
            # string representation
            if "<sbml" not in filename:
                raise IOError("The file with 'filename' does not exist, "
                              "or is not an SBML string. Provide the path to "
                              "an existing SBML file or a valid SBML string "
                              "representation: \n%s", filename)

            doc = libsbml.readSBMLFromString(filename)  # noqa: E501 type: libsbml.SBMLDocument

    elif hasattr(filename, "read"):
        # file handle
        doc = libsbml.readSBMLFromString(filename.read())  # noqa: E501 type: libsbml.SBMLDocument
    else:
        raise CobraSBMLError("Input type '%s' for 'filename' is not supported."
                             " Provide a path, SBML str, "
                             "or file handle.", type(filename))

    return doc