def search(self, number=None, *args, **kwargs):
        """
            Searches the elasticsearch instance to retrieve the requested documents.
        """
        search = self.create_search(*args, **kwargs)
        try:
            if number:
                response = search[0:number]
            else:
                args, _ = self.core_parser.parse_known_args()
                if args.number:
                    response = search[0:args.number]
                else:
                    response = search.scan()

            return [hit for hit in response]
        except NotFoundError:
            print_error("The index was not found, have you initialized the index?")
            return []
        except (ConnectionError, TransportError):
            print_error("Cannot connect to elasticsearch")
            return []