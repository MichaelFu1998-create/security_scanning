def check_reference(self, sequence_region=False, fasta_embedded=False, fasta_external=False, check_bounds=True, check_n=True, allowed_num_of_n=0, feature_types=('CDS',)):
        """
        Check seqid, bounds and the number of Ns in each feature using one or more reference sources.

        Seqid check: check if the seqid can be found in the reference sources.

        Bounds check: check the start and end fields of each features and log error if the values aren't within the seqid sequence length, requires at least one of these sources: ##sequence-region, embedded #FASTA, or external FASTA file.

        Ns check: count the number of Ns in each feature with the type specified in *line_types (default: 'CDS') and log an error if the number is greater than allowed_num_of_n (default: 0), requires at least one of these sources: embedded #FASTA, or external FASTA file.

        When called with all source parameters set as False (default), check all available sources, and log debug message if unable to perform a check due to none of the reference sources being available.

        If any source parameter is set to True, check only those sources marked as True, log error if those sources don't exist.

        :param sequence_region: check bounds using the ##sequence-region directive (default: False)
        :param fasta_embedded: check bounds using the embedded fasta specified by the ##FASTA directive (default: False)
        :param fasta_external: check bounds using the external fasta given by the self.parse_fasta_external (default: False)
        :param check_bounds: If False, don't run the bounds check (default: True)
        :param check_n: If False, don't run the Ns check (default: True)
        :param allowed_num_of_n: only report features with a number of Ns greater than the specified value (default: 0)
        :param feature_types: only check features of these feature_types, multiple types may be specified, if none are specified, check only 'CDS'
        :return: error_lines: a set of line_index(int) with errors detected by check_reference
        """
        # collect lines with errors in this set
        error_lines = set()
        # check if we have a parsed gff3
        if not self.lines:
            self.logger.debug('.parse(gff_file) before calling .check_bounds()')
            return error_lines
        # setup default line_types
        check_n_feature_types = set(feature_types)
        if len(check_n_feature_types) == 0:
            check_n_feature_types.add('CDS')
        # compile regex
        n_segments_finditer = re.compile(r'[Nn]+').finditer
        # check_all_sources mode
        check_all_sources = True
        if sequence_region or fasta_embedded or fasta_external:
            check_all_sources = False
        # get a list of line_data with valid start and end coordinates and unescape the seqid
        start_end_error_locations = set(('start', 'end', 'start,end'))
        valid_line_data_seqid = [(line_data, unquote(line_data['seqid'])) for line_data in self.lines if line_data['line_type'] == 'feature' and line_data['seqid'] != '.' and (not line_data['line_errors'] or not [error_info for error_info in line_data['line_errors'] if 'location' in error_info and error_info['location'] in start_end_error_locations])]
        checked_at_least_one_source = False
        # check directive
        # don't use any directives with errors
        valid_sequence_regions = dict([(unquote(line_data['seqid']), line_data) for line_data in self.lines if line_data['directive'] == '##sequence-region' and not line_data['line_errors']])
        unresolved_seqid = set()
        if (check_all_sources or sequence_region) and valid_sequence_regions:
            checked_at_least_one_source = True
            for line_data, seqid in valid_line_data_seqid:
                if seqid not in valid_sequence_regions and seqid not in unresolved_seqid:
                    unresolved_seqid.add(seqid)
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': u'Seqid not found in any ##sequence-region: {0:s}'.format(
                        seqid), 'error_type': 'BOUNDS', 'location': 'sequence_region'})
                    continue
                if line_data['start'] < valid_sequence_regions[seqid]['start']:
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': 'Start is less than the ##sequence-region start: %d' % valid_sequence_regions[seqid]['start'], 'error_type': 'BOUNDS', 'location': 'sequence_region'})
                if line_data['end'] > valid_sequence_regions[seqid]['end']:
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': 'End is greater than the ##sequence-region end: %d' % valid_sequence_regions[seqid]['end'], 'error_type': 'BOUNDS', 'location': 'sequence_region'})
        elif sequence_region:
            self.logger.debug('##sequence-region not found in GFF3')
        # check fasta_embedded
        unresolved_seqid = set()
        if (check_all_sources or fasta_embedded) and self.fasta_embedded:
            checked_at_least_one_source = True
            for line_data, seqid in valid_line_data_seqid:
                if seqid not in self.fasta_embedded and seqid not in unresolved_seqid:
                    unresolved_seqid.add(seqid)
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': 'Seqid not found in the embedded ##FASTA: %s' % seqid, 'error_type': 'BOUNDS', 'location': 'fasta_embedded'})
                    continue
                # check bounds
                if line_data['end'] > len(self.fasta_embedded[seqid]['seq']):
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': 'End is greater than the embedded ##FASTA sequence length: %d' % len(self.fasta_embedded[seqid]['seq']), 'error_type': 'BOUNDS', 'location': 'fasta_embedded'})
                # check n
                if check_n and line_data['type'] in check_n_feature_types:
                    """
                    >>> timeit("a.lower().count('n')", "import re; a = ('ASDKADSJHFIUDNNNNNNNnnnnSHFD'*50)")
                    5.540903252684302
                    >>> timeit("a.count('n'); a.count('N')", "import re; a = ('ASDKADSJHFIUDNNNNNNNnnnnSHFD'*50)")
                    2.3504867946058425
                    >>> timeit("re.findall('[Nn]+', a)", "import re; a = ('ASDKADSJHFIUDNNNNNNNnnnnSHFD'*50)")
                    30.60731204915959
                    """
                    n_count = self.fasta_embedded[seqid]['seq'].count('N', line_data['start'] - 1, line_data['end']) + self.fasta_embedded[seqid]['seq'].count('n', line_data['start'] - 1, line_data['end'])
                    if n_count > allowed_num_of_n:
                        # get detailed segments info
                        n_segments = [(m.start(), m.end() - m.start()) for m in n_segments_finditer(self.fasta_embedded[seqid]['seq'], line_data['start'] - 1, line_data['end'])]
                        n_segments_str = ['(%d, %d)' % (m[0], m[1]) for m in n_segments]
                        error_lines.add(line_data['line_index'])
                        self.add_line_error(line_data, {'message': 'Found %d Ns in %s feature of length %d using the embedded ##FASTA, consists of %d segment (start, length): %s' % (n_count, line_data['type'], line_data['end'] - line_data['start'], len(n_segments), ', '.join(n_segments_str)), 'error_type': 'N_COUNT', 'n_segments': n_segments, 'location': 'fasta_embedded'})
        elif fasta_embedded:
            self.logger.debug('Embedded ##FASTA not found in GFF3')
        # check fasta_external
        unresolved_seqid = set()
        if (check_all_sources or fasta_external) and self.fasta_external:
            checked_at_least_one_source = True
            for line_data, seqid in valid_line_data_seqid:
                if seqid not in self.fasta_external and seqid not in unresolved_seqid:
                    unresolved_seqid.add(seqid)
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': 'Seqid not found in the external FASTA file: %s' % seqid, 'error_type': 'BOUNDS', 'location': 'fasta_external'})
                    continue
                # check bounds
                if line_data['end'] > len(self.fasta_external[seqid]['seq']):
                    error_lines.add(line_data['line_index'])
                    self.add_line_error(line_data, {'message': 'End is greater than the external FASTA sequence length: %d' % len(self.fasta_external[seqid]['seq']), 'error_type': 'BOUNDS', 'location': 'fasta_external'})
                # check n
                if check_n and line_data['type'] in check_n_feature_types:
                    n_count = self.fasta_external[seqid]['seq'].count('N', line_data['start'] - 1, line_data['end']) + self.fasta_external[seqid]['seq'].count('n', line_data['start'] - 1, line_data['end'])
                    if n_count > allowed_num_of_n:
                        # get detailed segments info
                        n_segments = [(m.start(), m.end() - m.start()) for m in n_segments_finditer(self.fasta_external[seqid]['seq'], line_data['start'] - 1, line_data['end'])]
                        n_segments_str = ['(%d, %d)' % (m[0], m[1]) for m in n_segments]
                        error_lines.add(line_data['line_index'])
                        self.add_line_error(line_data, {'message': 'Found %d Ns in %s feature of length %d using the external FASTA, consists of %d segment (start, length): %s' % (n_count, line_data['type'], line_data['end'] - line_data['start'], len(n_segments), ', '.join(n_segments_str)), 'error_type': 'N_COUNT', 'n_segments': n_segments, 'location': 'fasta_external'})
        elif fasta_external:
            self.logger.debug('External FASTA file not given')
        if check_all_sources and not checked_at_least_one_source:
            self.logger.debug('Unable to perform bounds check, requires at least one of the following sources: ##sequence-region, embedded ##FASTA, or external FASTA file')
        return error_lines