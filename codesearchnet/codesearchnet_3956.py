def launch_R_script(template, arguments, output_function=None,
                    verbose=True, debug=False):
    """Launch an R script, starting from a template and replacing text in file
    before execution.

    Args:
        template (str): path to the template of the R script
        arguments (dict): Arguments that modify the template's placeholders
            with arguments
        output_function (function): Function to execute **after** the execution
            of the R script, and its output is returned by this function. Used
            traditionally as a function to retrieve the results of the
            execution.
        verbose (bool): Sets the verbosity of the R subprocess.
        debug (bool): If True, the generated scripts are not deleted.

    Return:
        Returns the output of the ``output_function`` if not `None`
        else `True` or `False` depending on whether the execution was
        successful.
    """
    id = str(uuid.uuid4())
    os.makedirs('/tmp/cdt_R_script_' + id + '/')
    try:
        scriptpath = '/tmp/cdt_R_script_' + id + '/instance_{}'.format(os.path.basename(template))
        copy(template, scriptpath)

        with fileinput.FileInput(scriptpath, inplace=True) as file:
            for line in file:
                mline = line
                for elt in arguments:
                    mline = mline.replace(elt, arguments[elt])
                print(mline, end='')

        if output_function is None:
            output = subprocess.call("Rscript --vanilla {}".format(scriptpath), shell=True,
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            if verbose:
                process = subprocess.Popen("Rscript --vanilla {}".format(scriptpath), shell=True)
            else:
                process = subprocess.Popen("Rscript --vanilla {}".format(scriptpath), shell=True,
                                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            process.wait()
            output = output_function()

    # Cleaning up
    except Exception as e:
        if not debug:
            rmtree('/tmp/cdt_R_script_' + id + '/')
        raise e
    except KeyboardInterrupt:
        if not debug:
            rmtree('/tmp/cdt_R_script_' + id + '/')
        raise KeyboardInterrupt
    if not debug:
        rmtree('/tmp/cdt_R_script_' + id + '/')
    return output