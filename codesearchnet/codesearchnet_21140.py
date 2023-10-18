def main():
    """
    Parse command line argument and
    output appropriate file type (csv or JSON)
    """
    parser = ArgumentParser()

    parser.add_argument(
        "-c", "--clinvarfile", dest="clinvarfile",
        help="ClinVar VCF file (either this or -C must be specified)",
        metavar="CLINVARFILE")
    parser.add_argument(
        "-C", "--clinvardir", dest="clinvardir",
        help="ClinVar VCF directory (either this or -c must be specified). " +
        "This option will use vcf2clinvar.clinvar_update to automatically " +
        "check and import the most recent ClinVar file to this directory.",
        metavar="CLINVARDIR")
    parser.add_argument(
        "-i", "--input", dest="inputfile",
        help="Input VCF file ['.vcf', '.vcf.gz', '.vcf.bz2']. " +
        "Uncompressed genome data is also accepted via stdin.",
        metavar="INPUT")
    parser.add_argument(
        "-t", "--type", dest="type", default='csv',
        help="Output report type ('csv' or 'json'). Defaults to csv. " +
        "CSV Report: Reports all genome variants matching ClinVar records, " +
        "and some summary ClinVar data from these records. Header lines " +
        "with metadata begin with '##'.\n" +
        "JSON Report: Reports genome variants matching ClinVar records " +
        "(no record information is included).",
        metavar="TYPE")
    parser.add_argument(
        "-n", "--notes", dest="notes",
        help="Notes (JSON format) to include in report. (JSON report only)",
        metavar="NOTES")
    parser.add_argument(
        "-g", "--genome-build", dest="build",
        help="Genome build to include in report ('b37' or 'b38').",
        metavar="GENOMEBUILD")
    options = parser.parse_args()

    version = os.popen("python setup.py --version").read().strip()

    if options.inputfile:
        if options.inputfile.endswith('.vcf'):
            input_genome_file = open(options.inputfile)
        elif options.inputfile.endswith('.vcf.gz'):
            input_genome_file = gzip.open(options.inputfile)
        elif options.inputfile.endswith('.vcf.bz2'):
            input_genome_file = bz2.BZ2File(options.inputfile)
        else:
            raise IOError("Genome filename expected to end with ''.vcf'," +
                          " '.vcf.gz', or '.vcf.bz2'.")
    elif not sys.stdin.isatty():
        input_genome_file = sys.stdin
    else:
        sys.stderr.write("Provide input VCF file\n")
        parser.print_help()
        sys.exit(1)

    if options.build and options.build in ['b37', 'b38']:
        build = options.build
    else:
        raise IOError("Input VCF genome build must be 'b37' or 'b38'.")

    if (not (options.clinvarfile or options.clinvardir) or
            (options.clinvarfile and options.clinvardir)):
        sys.stderr.write("Please provide either a ClinVar file or directory.")
        parser.print_help()
        sys.exit(1)
    if options.clinvarfile:
        clinvarfilename = options.clinvarfile
    elif options.clinvardir:
        clinvarfilename = get_latest_vcf_file(target_dir=options.clinvardir,
                                              build=build)
    if clinvarfilename.endswith('.vcf'):
        input_clinvar_file = open(options.clinvarfile)
    elif clinvarfilename.endswith('.vcf.gz'):
        input_clinvar_file = gzip.open(clinvarfilename)
    elif clinvarfilename.endswith('.vcf.bz2'):
        input_clinvar_file = bz2.BZ2File(clinvarfilename)
    else:
        raise IOError("ClinVar filename expected to end with '.vcf'," +
                      " '.vcf.gz', or '.vcf.bz2'.")

    if options.type not in ['csv', 'json']:
        raise IOError("Not a valid report type, must be 'csv' or 'json'.")
    if options.type == "csv":
        csv_report(input_genome_file=input_genome_file,
                   input_clinvar_file=input_clinvar_file,
                   build=build,
                   version=version)
    elif options.type == "json":
        notes_json = {}
        if options.notes:
            notes_json["parameter"] = options.notes
            try:
                notes_json = json.loads(options.notes)
            except:
                sys.stderr.write("Could not parse JSON notes field\n")
        json_report(input_genome_file=input_genome_file,
                    input_clinvar_file=input_clinvar_file,
                    build=build,
                    notes=notes_json,
                    version=version)