def check_phase(self):
        """
        1. get a list of CDS with the same parent
        2. sort according to strand
        3. calculate and validate phase
        """
        plus_minus = set(['+', '-'])
        for k, g in groupby(sorted([line for line in self.lines if  line['line_type'] == 'feature' and line['type'] == 'CDS' and 'Parent' in line['attributes']], key=lambda x: x['attributes']['Parent']), key=lambda x: x['attributes']['Parent']):
            cds_list = list(g)
            strand_set = list(set([line['strand'] for line in cds_list]))
            if len(strand_set) != 1:
                for line in cds_list:
                    self.add_line_error(line, {'message': 'Inconsistent CDS strand with parent: {0:s}'.format(k), 'error_type': 'STRAND'})
                continue
            if len(cds_list) == 1:
                if cds_list[0]['phase'] != 0:
                    self.add_line_error(cds_list[0], {'message': 'Wrong phase {0:d}, should be {1:d}'.format(cds_list[0]['phase'], 0), 'error_type': 'PHASE'})
                continue
            strand = strand_set[0]
            if strand not in plus_minus:
                # don't process unknown strands
                continue
            if strand == '-':
                # sort end descending
                sorted_cds_list = sorted(cds_list, key=lambda x: x['end'], reverse=True)
            else:
                sorted_cds_list = sorted(cds_list, key=lambda x: x['start'])
            phase = 0
            for line in sorted_cds_list:
                if line['phase'] != phase:
                    self.add_line_error(line, {'message': 'Wrong phase {0:d}, should be {1:d}'.format(line['phase'], phase), 'error_type': 'PHASE'})
                phase = (3 - ((line['end'] - line['start'] + 1 - phase) % 3)) % 3