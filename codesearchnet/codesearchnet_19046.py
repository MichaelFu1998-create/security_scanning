def report_read_counts(self, filename, grp_wise=False, reorder='as-is', notes=None):
        """
        Exports expected read counts

        :param filename: File name for output
        :param grp_wise: whether the report is at isoform level or gene level
        :param reorder: whether the report should be either 'decreasing' or 'increasing' order or just 'as-is'
        :return: Nothing but the method writes a file
        """
        expected_read_counts = self.probability.sum(axis=APM.Axis.READ)
        if grp_wise:
            lname = self.probability.gname
            expected_read_counts = expected_read_counts * self.grp_conv_mat
        else:
            lname = self.probability.lname
        total_read_counts = expected_read_counts.sum(axis=0)
        if reorder == 'decreasing':
            report_order = np.argsort(total_read_counts.flatten())
            report_order = report_order[::-1]
        elif reorder == 'increasing':
            report_order = np.argsort(total_read_counts.flatten())
        elif reorder == 'as-is':
            report_order = np.arange(len(lname))  # report in the original locus order
        cntdata = np.vstack((expected_read_counts, total_read_counts))
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