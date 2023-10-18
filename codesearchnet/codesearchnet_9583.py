def formats(input_formats, output_formats, debug=False):
    """List input and/or output formats."""
    if input_formats == output_formats:
        show_inputs, show_outputs = True, True
    else:
        show_inputs, show_outputs = input_formats, output_formats

    if show_inputs:
        click.echo("input formats:")
        for driver in available_input_formats():
            click.echo("- %s" % driver)
    if show_outputs:
        click.echo("output formats:")
        for driver in available_output_formats():
            click.echo("- %s" % driver)