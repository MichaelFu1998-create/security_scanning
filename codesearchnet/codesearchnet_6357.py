def _check(value, message):
    """
    Checks the libsbml return value and logs error messages.

    If 'value' is None, logs an error message constructed using
      'message' and then exits with status code 1. If 'value' is an integer,
      it assumes it is a libSBML return status code. If the code value is
      LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
      prints an error message constructed using 'message' along with text from
      libSBML explaining the meaning of the code, and exits with status code 1.

    """
    if value is None:
        LOGGER.error('Error: LibSBML returned a null value trying '
                     'to <' + message + '>.')
    elif type(value) is int:
        if value == libsbml.LIBSBML_OPERATION_SUCCESS:
            return
        else:
            LOGGER.error('Error encountered trying to <' + message + '>.')
            LOGGER.error('LibSBML error code {}: {}'.format(str(value),
                         libsbml.OperationReturnValue_toString(value).strip()))
    else:
        return