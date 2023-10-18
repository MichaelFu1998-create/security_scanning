def main():
    argparser = ArgumentParser()

    subparsers = argparser.add_subparsers(dest='selected_subparser')

    all_parser = subparsers.add_parser('all')
    elsevier_parser = subparsers.add_parser('elsevier')
    oxford_parser = subparsers.add_parser('oxford')
    springer_parser = subparsers.add_parser('springer')

    all_parser.add_argument('--update-credentials', action='store_true')

    elsevier_parser.add_argument('--run-locally', action='store_true')
    elsevier_parser.add_argument('--package-name')
    elsevier_parser.add_argument('--path')
    elsevier_parser.add_argument('--CONSYN', action='store_true')
    elsevier_parser.add_argument('--update-credentials', action='store_true')
    elsevier_parser.add_argument('--extract-nations', action='store_true')

    oxford_parser.add_argument('--dont-empty-ftp', action='store_true')
    oxford_parser.add_argument('--package-name')
    oxford_parser.add_argument('--path')
    oxford_parser.add_argument('--update-credentials', action='store_true')
    oxford_parser.add_argument('--extract-nations', action='store_true')

    springer_parser.add_argument('--package-name')
    springer_parser.add_argument('--path')
    springer_parser.add_argument('--update-credentials', action='store_true')
    springer_parser.add_argument('--extract-nations', action='store_true')

    '''
    Transforms the argparse arguments from Namespace to dict and then to Bunch
    Therefore it is not necessary to access the arguments using the dict syntax
    The settings can be called like regular vars on the settings object
    '''

    settings = Bunch(vars(argparser.parse_args()))

    call_package(settings)