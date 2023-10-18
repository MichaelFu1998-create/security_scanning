def _run_gies(self, data, fixedGaps=None, verbose=True):
        """Setting up and running GIES with all arguments."""
        # Run gies
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_gies' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_gies' + id + '/'

        def retrieve_result():
            return read_csv('/tmp/cdt_gies' + id + '/result.csv', delimiter=',').values

        try:
            data.to_csv('/tmp/cdt_gies' + id + '/data.csv', header=False, index=False)
            if fixedGaps is not None:
                fixedGaps.to_csv('/tmp/cdt_gies' + id + '/fixedgaps.csv', index=False, header=False)
                self.arguments['{SKELETON}'] = 'TRUE'
            else:
                self.arguments['{SKELETON}'] = 'FALSE'

            gies_result = launch_R_script("{}/R_templates/gies.R".format(os.path.dirname(os.path.realpath(__file__))),
                                          self.arguments, output_function=retrieve_result, verbose=verbose)
        # Cleanup
        except Exception as e:
            rmtree('/tmp/cdt_gies' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_gies' + id + '/')
            raise KeyboardInterrupt
        rmtree('/tmp/cdt_gies' + id + '')
        return gies_result