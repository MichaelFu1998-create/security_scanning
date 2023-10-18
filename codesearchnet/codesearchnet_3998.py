def _run_pc(self, data, fixedEdges=None, fixedGaps=None, verbose=True):
        """Setting up and running pc with all arguments."""
        # Checking coherence of arguments
        # print(self.arguments)
        if (self.arguments['{CITEST}'] == self.dir_CI_test['hsic']
           and self.arguments['{METHOD_INDEP}'] == self.dir_method_indep['corr']):
            warnings.warn('Selected method for indep is unfit for the hsic test,'
                          ' setting the hsic.gamma method.')
            self.arguments['{METHOD_INDEP}'] = self.dir_method_indep['hsic_gamma']

        elif (self.arguments['{CITEST}'] == self.dir_CI_test['gaussian']
              and self.arguments['{METHOD_INDEP}'] != self.dir_method_indep['corr']):
            warnings.warn('Selected method for indep is unfit for the selected test,'
                          ' setting the classic correlation-based method.')
            self.arguments['{METHOD_INDEP}'] = self.dir_method_indep['corr']

        # Run PC
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_pc' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_pc' + id + '/'

        def retrieve_result():
            return read_csv('/tmp/cdt_pc' + id + '/result.csv', delimiter=',').values

        try:
            data.to_csv('/tmp/cdt_pc' + id + '/data.csv', header=False, index=False)
            if fixedGaps is not None and fixedEdges is not None:
                fixedGaps.to_csv('/tmp/cdt_pc' + id + '/fixedgaps.csv', index=False, header=False)
                fixedEdges.to_csv('/tmp/cdt_pc' + id + '/fixededges.csv', index=False, header=False)
                self.arguments['{SKELETON}'] = 'TRUE'
            else:
                self.arguments['{SKELETON}'] = 'FALSE'

            pc_result = launch_R_script("{}/R_templates/pc.R".format(os.path.dirname(os.path.realpath(__file__))),
                                        self.arguments, output_function=retrieve_result, verbose=verbose)
        # Cleanup
        except Exception as e:
            rmtree('/tmp/cdt_pc' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_pc' + id + '/')
            raise KeyboardInterrupt
        rmtree('/tmp/cdt_pc' + id + '')
        return pc_result