def _create_parameter(model, pid, value, sbo=None, constant=True, units=None,
                      flux_udef=None):
    """Create parameter in SBML model."""
    parameter = model.createParameter()  # type: libsbml.Parameter
    parameter.setId(pid)
    parameter.setValue(value)
    parameter.setConstant(constant)
    if sbo:
        parameter.setSBOTerm(sbo)
    if units:
        parameter.setUnits(flux_udef.getId())