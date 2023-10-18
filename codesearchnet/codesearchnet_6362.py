def validate_sbml_model(filename,
                        check_model=True,
                        internal_consistency=True,
                        check_units_consistency=False,
                        check_modeling_practice=False, **kwargs):
    """Validate SBML model and returns the model along with a list of errors.

    Parameters
    ----------
    filename : str
        The filename (or SBML string) of the SBML model to be validated.
    internal_consistency: boolean {True, False}
        Check internal consistency.
    check_units_consistency: boolean {True, False}
        Check consistency of units.
    check_modeling_practice: boolean {True, False}
        Check modeling practise.
    check_model: boolean {True, False}
        Whether to also check some basic model properties such as reaction
        boundaries and compartment formulas.

    Returns
    -------
    (model, errors)
    model : :class:`~cobra.core.Model.Model` object
        The cobra model if the file could be read successfully or None
        otherwise.
    errors : dict
        Warnings and errors grouped by their respective types.

    Raises
    ------
    CobraSBMLError
    """
    # Errors and warnings are grouped based on their type. SBML_* types are
    # from the libsbml validator. COBRA_* types are from the cobrapy SBML
    # parser.
    keys = (
        "SBML_FATAL",
        "SBML_ERROR",
        "SBML_SCHEMA_ERROR",
        "SBML_WARNING",

        "COBRA_FATAL",
        "COBRA_ERROR",
        "COBRA_WARNING",
        "COBRA_CHECK",
    )
    errors = {key: [] for key in keys}

    # [1] libsbml validation
    doc = _get_doc_from_filename(filename)  # type: libsbml.SBMLDocument

    # set checking of units & modeling practise
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY,
                             check_units_consistency)
    doc.setConsistencyChecks(libsbml.LIBSBML_CAT_MODELING_PRACTICE,
                             check_modeling_practice)

    # check internal consistency
    if internal_consistency:
        doc.checkInternalConsistency()
    doc.checkConsistency()

    for k in range(doc.getNumErrors()):
        e = doc.getError(k)  # type: libsbml.SBMLError
        msg = _error_string(e, k=k)
        sev = e.getSeverity()
        if sev == libsbml.LIBSBML_SEV_FATAL:
            errors["SBML_FATAL"].append(msg)
        elif sev == libsbml.LIBSBML_SEV_ERROR:
            errors["SBML_ERROR"].append(msg)
        elif sev == libsbml.LIBSBML_SEV_SCHEMA_ERROR:
            errors["SBML_SCHEMA_ERROR"].append(msg)
        elif sev == libsbml.LIBSBML_SEV_WARNING:
            errors["SBML_WARNING"].append(msg)

    # [2] cobrapy validation (check that SBML can be read into model)
    # all warnings generated while loading will be logged as errors
    log_stream = StringIO()
    stream_handler = logging.StreamHandler(log_stream)
    formatter = logging.Formatter('%(levelname)s:%(message)s')
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    LOGGER.addHandler(stream_handler)
    LOGGER.propagate = False

    try:
        # read model and allow additional parser arguments
        model = _sbml_to_model(doc, **kwargs)
    except CobraSBMLError as e:
        errors["COBRA_ERROR"].append(str(e))
        return None, errors
    except Exception as e:
        errors["COBRA_FATAL"].append(str(e))
        return None, errors

    cobra_errors = log_stream.getvalue().split("\n")
    for cobra_error in cobra_errors:
        tokens = cobra_error.split(":")
        error_type = tokens[0]
        error_msg = ":".join(tokens[1:])

        if error_type == "WARNING":
            errors["COBRA_WARNING"].append(error_msg)
        elif error_type == "ERROR":
            errors["COBRA_ERROR"].append(error_msg)

    # remove stream handler
    LOGGER.removeHandler(stream_handler)
    LOGGER.propagate = True

    # [3] additional model tests
    if check_model:
        errors["COBRA_CHECK"].extend(
            check_metabolite_compartment_formula(model)
        )

    for key in ["SBML_FATAL", "SBML_ERROR", "SBML_SCHEMA_ERROR"]:
        if len(errors[key]) > 0:
            LOGGER.error("SBML errors in validation, check error log "
                         "for details.")
            break
    for key in ["SBML_WARNING"]:
        if len(errors[key]) > 0:
            LOGGER.error("SBML warnings in validation, check error log "
                         "for details.")
            break
    for key in ["COBRA_FATAL", "COBRA_ERROR"]:
        if len(errors[key]) > 0:
            LOGGER.error("COBRA errors in validation, check error log "
                         "for details.")
            break
    for key in ["COBRA_WARNING", "COBRA_CHECK"]:
        if len(errors[key]) > 0:
            LOGGER.error("COBRA warnings in validation, check error log "
                         "for details.")
            break

    return model, errors