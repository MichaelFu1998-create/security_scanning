def main():
    """
        Main credentials tool
    """
    cred_search = CredentialSearch()
    arg = argparse.ArgumentParser(parents=[cred_search.argparser], conflict_handler='resolve')
    arg.add_argument('-c', '--count', help="Only show the number of results", action="store_true")
    arguments = arg.parse_args()

    if arguments.count:
        print_line("Number of credentials: {}".format(cred_search.argument_count()))
    else:
        response = cred_search.get_credentials()
        for hit in response:
            print_json(hit.to_dict(include_meta=True))