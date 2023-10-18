def tv_to_rdf(infile_name, outfile_name):
    """
    Convert a SPDX file from tag/value format to RDF format.
    Return True on sucess, False otherwise.
    """
    parser = Parser(Builder(), StandardLogger())
    parser.build()
    with open(infile_name) as infile:
        data = infile.read()
        document, error = parser.parse(data)
        if not error:
            with open(outfile_name, mode='w') as outfile:
                write_document(document, outfile)
            return True
        else:
            print('Errors encountered while parsing RDF file.')
            messages = []
            document.validate(messages)
            print('\n'.join(messages))
            return False