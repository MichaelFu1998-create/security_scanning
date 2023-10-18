def run(self, model, tol=0.001, max_iters=999, verbose=True):
        """
        Runs EM iterations

        :param model: Normalization model (1: Gene->Allele->Isoform, 2: Gene->Isoform->Allele, 3: Gene->Isoform*Allele, 4: Gene*Isoform*Allele)
        :param tol: Tolerance for termination
        :param max_iters: Maximum number of iterations until termination
        :param verbose: Display information on how EM is running
        :return: Nothing (as it performs in-place operations)
        """
        orig_err_states = np.seterr(all='raise')
        np.seterr(under='ignore')
        if verbose:
            print
            print "Iter No  Time (hh:mm:ss)    Total change (TPM)  "
            print "-------  ---------------  ----------------------"
        num_iters = 0
        err_sum = 1000000.0
        time0 = time.time()
        target_err = 1000000.0 * tol
        while err_sum > target_err and num_iters < max_iters:
            prev_isoform_expression = self.get_allelic_expression().sum(axis=0)
            prev_isoform_expression *= (1000000.0 / prev_isoform_expression.sum())
            self.update_allelic_expression(model=model)
            curr_isoform_expression = self.get_allelic_expression().sum(axis=0)
            curr_isoform_expression *= (1000000.0 / curr_isoform_expression.sum())
            err = np.abs(curr_isoform_expression - prev_isoform_expression)
            err_sum = err.sum()
            num_iters += 1
            if verbose:
                time1 = time.time()
                delmin, s = divmod(int(time1 - time0), 60)
                h, m = divmod(delmin, 60)
                print " %5d      %4d:%02d:%02d     %9.1f / 1000000" % (num_iters, h, m, s, err_sum)