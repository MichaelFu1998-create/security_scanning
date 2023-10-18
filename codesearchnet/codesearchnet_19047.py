def report_depths(self, filename, tpm=True, grp_wise=False, reorder='as-is', notes=None):
        """
        Exports expected depths

        :param filename: File name for output
        :param grp_wise: whether the report is at isoform level or gene level
        :param reorder: whether the report should be either 'decreasing' or 'increasing' order or just 'as-is'
        :return: Nothing but the method writes a file
        """
        if grp_wise:
            lname = self.probability.gname
            depths = self.allelic_expression * self.grp_conv_mat
        else:
            lname = self.probability.lname
            depths = self.allelic_expression
        if tpm:
            depths *= (1000000.0 / depths.sum())
        total_depths = depths.sum(axis=0)
        if reorder == 'decreasing':
            report_order = np.argsort(total_depths.flatten())
            report_order = report_order[::-1]
        elif reorder == 'increasing':
            report_order = np.argsort(total_depths.flatten())
        elif reorder == 'as-is':
            report_order = np.arange(len(lname))  # report in the original locus order
        cntdata = np.vstack((depths, total_depths))
        fhout = open(filename, 'w')
        fhout.write("locus\t" + "\t".join(self.probability.hname) + "\ttotal")
        if notes is not None:
            fhout.write("\tnotes")
        fhout.write("\n")
        for locus_id in report_order:
            lname_cur = lname[locus_id]
            fhout.write("\t".join([lname_cur] + map(str, cntdata[:, locus_id].ravel())))
            if notes is not None:
                fhout.write("\t%s" % notes[lname_cur])
            fhout.write("\n")
        fhout.close()