def total_yield(input_fluxes, input_elements, output_flux, output_elements):
    """
    Compute total output per input unit.

    Units are typically mol carbon atoms or gram of source and product.

    Parameters
    ----------
    input_fluxes : list
        A list of input reaction fluxes in the same order as the
        ``input_components``.
    input_elements : list
        A list of reaction components which are in turn list of numbers.
    output_flux : float
        The output flux value.
    output_elements : list
        A list of stoichiometrically weighted output reaction components.

    Returns
    -------
    float
        The ratio between output (mol carbon atoms or grams of product) and
        input (mol carbon atoms or grams of source compounds).
    """

    carbon_input_flux = sum(
        total_components_flux(flux, components, consumption=True)
        for flux, components in zip(input_fluxes, input_elements))
    carbon_output_flux = total_components_flux(
        output_flux, output_elements, consumption=False)
    try:
        return carbon_output_flux / carbon_input_flux
    except ZeroDivisionError:
        return nan