def sequence(self, line_data, child_type=None, reference=None):
        """
        Get the sequence of line_data, according to the columns 'seqid', 'start', 'end', 'strand'.
        Requires fasta reference.
        When used on 'mRNA' type line_data, child_type can be used to specify which kind of sequence to return:
        * child_type=None:  pre-mRNA, returns the sequence of line_data from start to end, reverse complement according to strand. (default)
        * child_type='exon':  mature mRNA, concatenates the sequences of children type 'exon'.
        * child_type='CDS':  coding sequence, concatenates the sequences of children type 'CDS'. Use the helper
                             function translate(seq) on the returned value to obtain the protein sequence.

        :param line_data: line_data(dict) with line_data['line_index'] or line_index(int)
        :param child_type: None or feature type(string)
        :param reference: If None, will use self.fasta_external or self.fasta_embedded(dict)
        :return: sequence(string)
        """
        # get start node
        reference = reference or self.fasta_external or self.fasta_embedded
        if not reference:
            raise Exception('External or embedded fasta reference needed')
        try:
            line_index = line_data['line_index']
        except TypeError:
            line_index = self.lines[line_data]['line_index']
        ld = self.lines[line_index]
        if ld['type'] != 'feature':
            return None
        seq = reference[ld['seqid']][ld['start']-1:ld['end']]
        if ld['strand'] == '-':
            seq = complement(seq[::-1])
        return seq