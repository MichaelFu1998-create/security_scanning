def NetMHC(alleles,
           default_peptide_lengths=[9],
           program_name="netMHC"):
    """
    This function wraps NetMHC3 and NetMHC4 to automatically detect which class
    to use. Currently based on running the '-h' command and looking for
    discriminating substrings between the versions.
    """
    # run NetMHC's help command and parse discriminating substrings out of
    # the resulting str output
    with open(os.devnull, 'w') as devnull:
        help_output = check_output([program_name, "-h"], stderr=devnull)
    help_output_str = help_output.decode("ascii", "ignore")

    substring_to_netmhc_class = {
        "-listMHC": NetMHC4,
        "--Alleles": NetMHC3,
    }

    successes = []

    for substring, netmhc_class in substring_to_netmhc_class.items():
        if substring in help_output_str:
            successes.append(netmhc_class)

    if len(successes) > 1:
        raise SystemError("Command %s is valid for multiple NetMHC versions. "
                          "This is likely an mhctools bug." % program_name)
    if len(successes) == 0:
        raise SystemError("Command %s is not a valid way of calling any NetMHC software."
                          % program_name)

    netmhc_class = successes[0]
    return netmhc_class(
        alleles=alleles,
        default_peptide_lengths=default_peptide_lengths,
        program_name=program_name)