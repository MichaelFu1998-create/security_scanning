def parse(self, gff_file, strict=False):
        """Parse the gff file into the following data structures:

        * lines(list of line_data(dict))
            - line_index(int): the index in lines
            - line_raw(str)
            - line_type(str in ['feature', 'directive', 'comment', 'blank', 'unknown'])
            - line_errors(list of str): a list of error messages
            - line_status(str in ['normal', 'modified', 'removed'])
            - parents(list of feature(list of line_data(dict))): may have multiple parents
            - children(list of line_data(dict))
            - extra fields depending on line_type
            * directive
                - directive(str in ['##gff-version', '##sequence-region', '##feature-ontology', '##attribute-ontology', '##source-ontology', '##species', '##genome-build', '###', '##FASTA'])
                - extra fields depending on directive
            * feature
                - seqid(str): must escape any characters not in the set [a-zA-Z0-9.:^*$@!+_?-|] using RFC 3986 Percent-Encoding
                - source(str)
                - type(str in so_types)
                - start(int)
                - end(int)
                - score(float)
                - strand(str in ['+', '-', '.', '?'])
                - phase(int in [0, 1, 2])
                - attributes(dict of tag(str) to value)
                    - ID(str)
                    - Name(str)
                    - Alias(list of str): multi value
                    - Parent(list of str): multi value
                    - Target(dict)
                        - target_id(str)
                        - start(int)
                        - end(int)
                        - strand(str in ['+', '-', ''])
                    - Gap(str): CIGAR format
                    - Derives_from(str)
                    - Note(list of str): multi value
                    - Dbxref(list of str): multi value
                    - Ontology_term(list of str): multi value
                    - Is_circular(str in ['true'])
            * fasta_dict(dict of id(str) to sequence_item(dict))
                - id(str)
                - header(str)
                - seq(str)
                - line_length(int)

        * features(dict of feature_id(str in line_data['attributes']['ID']) to feature(list of line_data(dict)))

        A feature is a list of line_data(dict), since all lines that share an ID collectively represent a single feature.

        During serialization, line_data(dict) references should be converted into line_index(int)

        :param gff_file: a string path or file object
        :param strict: when true, throw exception on syntax and format errors. when false, use best effort to finish parsing while logging errors
        """
        valid_strand = set(('+', '-', '.', '?'))
        valid_phase = set((0, 1, 2))
        multi_value_attributes = set(('Parent', 'Alias', 'Note', 'Dbxref', 'Ontology_term'))
        valid_attribute_target_strand = set(('+', '-', ''))
        reserved_attributes = set(('ID', 'Name', 'Alias', 'Parent', 'Target', 'Gap', 'Derives_from', 'Note', 'Dbxref', 'Ontology_term', 'Is_circular'))

        # illegal character check
        # Literal use of tab, newline, carriage return, the percent (%) sign, and control characters must be encoded using RFC 3986 Percent-Encoding; no other characters may be encoded.
        # control characters: \x00-\x1f\x7f this includes tab(\x09), newline(\x0a), carriage return(\x0d)
        # seqid may contain any characters, but must escape any characters not in the set [a-zA-Z0-9.:^*$@!+_?-|]
        # URL escaping rules are used for tags or values containing the following characters: ",=;".
        #>>> timeit("unescaped_seqid('Un.7589')", "import re; unescaped_seqid = re.compile(r'[^a-zA-Z0-9.:^*$@!+_?|%-]|%(?![0-9a-fA-F]{2})').search")
        #0.4128372745785036
        #>>> timeit("unescaped_seqid2('Un.7589')", "import re; unescaped_seqid2 = re.compile(r'^([a-zA-Z0-9.:^*$@!+_?|-]|%[0-9a-fA-F]{2})+$').search")
        #0.9012313532265175
        unescaped_seqid = re.compile(r'[^a-zA-Z0-9.:^*$@!+_?|%-]|%(?![0-9a-fA-F]{2})').search
        unescaped_field = re.compile(r'[\x00-\x1f\x7f]|%(?![0-9a-fA-F]{2})').search

        gff_fp = gff_file
        if isinstance(gff_file, str):
            gff_fp = open(gff_file, 'r')

        lines = []
        current_line_num = 1 # line numbers start at 1
        features = defaultdict(list)
        # key = the unresolved id, value = a list of line_data(dict)
        unresolved_parents = defaultdict(list)

        for line_raw in gff_fp:
            line_data = {
                'line_index': current_line_num - 1,
                'line_raw': line_raw,
                'line_status': 'normal',
                'parents': [],
                'children': [],
                'line_type': '',
                'directive': '',
                'line_errors': [],
                'type': '',
            }
            line_strip = line_raw.strip()
            if line_strip != line_raw[:len(line_strip)]:
                self.add_line_error(line_data, {'message': 'White chars not allowed at the start of a line', 'error_type': 'FORMAT', 'location': ''})
            if current_line_num == 1 and not line_strip.startswith('##gff-version'):
                self.add_line_error(line_data, {'message': '"##gff-version" missing from the first line', 'error_type': 'FORMAT', 'location': ''})
            if len(line_strip) == 0:
                line_data['line_type'] = 'blank'
                continue
            if line_strip.startswith('##'):
                line_data['line_type'] = 'directive'
                if line_strip.startswith('##sequence-region'):
                    # ##sequence-region seqid start end
                    # This element is optional, but strongly encouraged because it allows parsers to perform bounds checking on features.
                    # only one ##sequence-region directive may be given for any given seqid
                    # all features on that landmark feature (having that seqid) must be contained within the range defined by that ##sequence-region diretive. An exception to this rule is allowed when a landmark feature is marked with the Is_circular attribute.
                    line_data['directive'] = '##sequence-region'
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 3:
                        self.add_line_error(line_data, {'message': 'Expecting 3 fields, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        line_data['seqid'] = tokens[0]
                        # check for duplicate ##sequence-region seqid
                        if [True for d in lines if ('directive' in d and d['directive'] == '##sequence-region' and 'seqid' in d and d['seqid'] == line_data['seqid'])]:
                            self.add_line_error(line_data, {'message': '##sequence-region seqid: "%s" may only appear once' % line_data['seqid'], 'error_type': 'FORMAT', 'location': ''})
                        try:
                            all_good = True
                            try:
                                line_data['start'] = int(tokens[1])
                                if line_data['start'] < 1:
                                    self.add_line_error(line_data, {'message': 'Start is not a valid 1-based integer coordinate: "%s"' % tokens[1], 'error_type': 'FORMAT', 'location': ''})
                            except ValueError:
                                all_good = False
                                self.add_line_error(line_data, {'message': 'Start is not a valid integer: "%s"' % tokens[1], 'error_type': 'FORMAT', 'location': ''})
                                line_data['start'] = tokens[1]
                            try:
                                line_data['end'] = int(tokens[2])
                                if line_data['end'] < 1:
                                    self.add_line_error(line_data, {'message': 'End is not a valid 1-based integer coordinate: "%s"' % tokens[2], 'error_type': 'FORMAT', 'location': ''})
                            except ValueError:
                                all_good = False
                                self.add_line_error(line_data, {'message': 'End is not a valid integer: "%s"' % tokens[2], 'error_type': 'FORMAT', 'location': ''})
                                line_data['start'] = tokens[2]
                            # if all_good then both start and end are int, so we can check if start is not less than or equal to end
                            if all_good and line_data['start'] > line_data['end']:
                                self.add_line_error(line_data, {'message': 'Start is not less than or equal to end', 'error_type': 'FORMAT', 'location': ''})
                        except IndexError:
                            pass
                elif line_strip.startswith('##gff-version'):
                    # The GFF version, always 3 in this specification must be present, must be the topmost line of the file and may only appear once in the file.
                    line_data['directive'] = '##gff-version'
                    # check if it appeared before
                    if [True for d in lines if ('directive' in d and d['directive'] == '##gff-version')]:
                        self.add_line_error(line_data, {'message': '##gff-version missing from the first line', 'error_type': 'FORMAT', 'location': ''})
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 1:
                        self.add_line_error(line_data, {'message': 'Expecting 1 field, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        try:
                            line_data['version'] = int(tokens[0])
                            if line_data['version'] != 3:
                                self.add_line_error(line_data, {'message': 'Version is not "3": "%s"' % tokens[0], 'error_type': 'FORMAT', 'location': ''})
                        except ValueError:
                            self.add_line_error(line_data, {'message': 'Version is not a valid integer: "%s"' % tokens[0], 'error_type': 'FORMAT', 'location': ''})
                            line_data['version'] = tokens[0]
                elif line_strip.startswith('###'):
                    # This directive (three # signs in a row) indicates that all forward references to feature IDs that have been seen to this point have been resolved.
                    line_data['directive'] = '###'
                elif line_strip.startswith('##FASTA'):
                    # This notation indicates that the annotation portion of the file is at an end and that the
                    # remainder of the file contains one or more sequences (nucleotide or protein) in FASTA format.
                    line_data['directive'] = '##FASTA'
                    self.logger.info('Reading embedded ##FASTA sequence')
                    self.fasta_embedded, count = fasta_file_to_dict(gff_fp)
                    self.logger.info('%d sequences read' % len(self.fasta_embedded))
                elif line_strip.startswith('##feature-ontology'):
                    # ##feature-ontology URI
                    # This directive indicates that the GFF3 file uses the ontology of feature types located at the indicated URI or URL.
                    line_data['directive'] = '##feature-ontology'
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 1:
                        self.add_line_error(line_data, {'message': 'Expecting 1 field, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        line_data['URI'] = tokens[0]
                elif line_strip.startswith('##attribute-ontology'):
                    # ##attribute-ontology URI
                    # This directive indicates that the GFF3 uses the ontology of attribute names located at the indicated URI or URL.
                    line_data['directive'] = '##attribute-ontology'
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 1:
                        self.add_line_error(line_data, {'message': 'Expecting 1 field, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        line_data['URI'] = tokens[0]
                elif line_strip.startswith('##source-ontology'):
                    # ##source-ontology URI
                    # This directive indicates that the GFF3 uses the ontology of source names located at the indicated URI or URL.
                    line_data['directive'] = '##source-ontology'
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 1:
                        self.add_line_error(line_data, {'message': 'Expecting 1 field, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        line_data['URI'] = tokens[0]
                elif line_strip.startswith('##species'):
                    # ##species NCBI_Taxonomy_URI
                    # This directive indicates the species that the annotations apply to.
                    line_data['directive'] = '##species'
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 1:
                        self.add_line_error(line_data, {'message': 'Expecting 1 field, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        line_data['NCBI_Taxonomy_URI'] = tokens[0]
                elif line_strip.startswith('##genome-build'):
                    # ##genome-build source buildName
                    # The genome assembly build name used for the coordinates given in the file.
                    line_data['directive'] = '##genome-build'
                    tokens = list(line_strip.split()[1:])
                    if len(tokens) != 2:
                        self.add_line_error(line_data, {'message': 'Expecting 2 fields, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                    if len(tokens) > 0:
                        line_data['source'] = tokens[0]
                        try:
                            line_data['buildName'] = tokens[1]
                        except IndexError:
                            pass
                else:
                    self.add_line_error(line_data, {'message': 'Unknown directive', 'error_type': 'FORMAT', 'location': ''})
                    tokens = list(line_strip.split())
                    line_data['directive'] = tokens[0]
            elif line_strip.startswith('#'):
                line_data['line_type'] = 'comment'
            else:
                # line_type may be a feature or unknown
                line_data['line_type'] = 'feature'
                tokens = list(map(str.strip, line_raw.split('\t')))
                if len(tokens) != 9:
                    self.add_line_error(line_data, {'message': 'Features should contain 9 fields, got %d: %s' % (len(tokens) - 1, repr(tokens[1:])), 'error_type': 'FORMAT', 'location': ''})
                for i, t in enumerate(tokens):
                    if not t:
                        self.add_line_error(line_data, {'message': 'Empty field: %d, must have a "."' % (i + 1), 'error_type': 'FORMAT', 'location': ''})
                try:
                    line_data['seqid'] = tokens[0]
                    if unescaped_seqid(tokens[0]):
                        self.add_line_error(line_data, {'message': 'Seqid must escape any characters not in the set [a-zA-Z0-9.:^*$@!+_?-|]: "%s"' % tokens[0], 'error_type': 'FORMAT', 'location': ''})
                    line_data['source'] = tokens[1]
                    if unescaped_field(tokens[1]):
                        self.add_line_error(line_data, {'message': 'Source must escape the percent (%%) sign and any control characters: "%s"' % tokens[1], 'error_type': 'FORMAT', 'location': ''})
                    line_data['type'] = tokens[2]
                    if unescaped_field(tokens[2]):
                        self.add_line_error(line_data, {'message': 'Type must escape the percent (%%) sign and any control characters: "%s"' % tokens[2], 'error_type': 'FORMAT', 'location': ''})
                    all_good = True
                    try:
                        line_data['start'] = int(tokens[3])
                        if line_data['start'] < 1:
                            self.add_line_error(line_data, {'message': 'Start is not a valid 1-based integer coordinate: "%s"' % tokens[3], 'error_type': 'FORMAT', 'location': 'start'})
                    except ValueError:
                        all_good = False
                        line_data['start'] = tokens[3]
                        if line_data['start'] != '.':
                            self.add_line_error(line_data, {'message': 'Start is not a valid integer: "%s"' % line_data['start'], 'error_type': 'FORMAT', 'location': 'start'})
                    try:
                        line_data['end'] = int(tokens[4])
                        if line_data['end'] < 1:
                            self.add_line_error(line_data, {'message': 'End is not a valid 1-based integer coordinate: "%s"' % tokens[4], 'error_type': 'FORMAT', 'location': 'end'})
                    except ValueError:
                        all_good = False
                        line_data['end'] = tokens[4]
                        if line_data['end'] != '.':
                            self.add_line_error(line_data, {'message': 'End is not a valid integer: "%s"' % line_data['end'], 'error_type': 'FORMAT', 'location': 'end'})
                    # if all_good then both start and end are int, so we can check if start is not less than or equal to end
                    if all_good and line_data['start'] > line_data['end']:
                        self.add_line_error(line_data, {'message': 'Start is not less than or equal to end', 'error_type': 'FORMAT', 'location': 'start,end'})
                    try:
                        line_data['score'] = float(tokens[5])
                    except ValueError:
                        line_data['score'] = tokens[5]
                        if line_data['score'] != '.':
                            self.add_line_error(line_data, {'message': 'Score is not a valid floating point number: "%s"' % line_data['score'], 'error_type': 'FORMAT', 'location': ''})
                    line_data['strand'] = tokens[6]
                    if line_data['strand'] not in valid_strand: # set(['+', '-', '.', '?'])
                        self.add_line_error(line_data, {'message': 'Strand has illegal characters: "%s"' % tokens[6], 'error_type': 'FORMAT', 'location': ''})
                    try:
                        line_data['phase'] = int(tokens[7])
                        if line_data['phase'] not in valid_phase: # set([0, 1, 2])
                            self.add_line_error(line_data, {'message': 'Phase is not 0, 1, or 2: "%s"' % tokens[7], 'error_type': 'FORMAT', 'location': ''})
                    except ValueError:
                        line_data['phase'] = tokens[7]
                        if line_data['phase'] != '.':
                            self.add_line_error(line_data, {'message': 'Phase is not a valid integer: "%s"' % line_data['phase'], 'error_type': 'FORMAT', 'location': ''})
                        elif line_data['type'] == 'CDS':
                            self.add_line_error(line_data, {'message': 'Phase is required for all CDS features', 'error_type': 'FORMAT', 'location': ''})
                    # parse attributes, ex: ID=exon00003;Parent=mRNA00001,mRNA00003;Name=EXON.1
                    # URL escaping rules are used for tags or values containing the following characters: ",=;". Spaces are allowed in this field, but tabs must be replaced with the %09 URL escape.
                    # Note that attribute names are case sensitive. "Parent" is not the same as "parent".
                    # All attributes that begin with an uppercase letter are reserved for later use. Attributes that begin with a lowercase letter can be used freely by applications.
                    if unescaped_field(tokens[8]):
                        self.add_line_error(line_data, {'message': 'Attributes must escape the percent (%) sign and any control characters', 'error_type': 'FORMAT', 'location': ''})
                    attribute_tokens = tuple(tuple(t for t in a.split('=')) for a in tokens[8].split(';') if a)
                    line_data['attributes'] = {}
                    if len(attribute_tokens) == 1 and len(attribute_tokens[0]) == 1 and attribute_tokens[0][0] == '.':
                        pass # no attributes
                    else:
                        for a in attribute_tokens:
                            if len(a) != 2:
                                self.add_line_error(line_data, {'message': 'Attributes must contain one and only one equal (=) sign: "%s"' % ('='.join(a)), 'error_type': 'FORMAT', 'location': ''})
                            try:
                                tag, value = a
                            except ValueError:
                                tag, value = a[0], ''
                            if not tag:
                                self.add_line_error(line_data, {'message': 'Empty attribute tag: "%s"' % '='.join(a), 'error_type': 'FORMAT', 'location': ''})
                            if not value.strip():
                                self.add_line_error(line_data, {'message': 'Empty attribute value: "%s"' % '='.join(a), 'error_type': 'FORMAT', 'location': ''}, log_level=logging.WARNING)
                            if tag in line_data['attributes']:
                                self.add_line_error(line_data, {'message': 'Found multiple attribute tags: "%s"' % tag, 'error_type': 'FORMAT', 'location': ''})
                            if tag in multi_value_attributes: # set(['Parent', 'Alias', 'Note', 'Dbxref', 'Ontology_term'])
                                if value.find(', ') >= 0:
                                    self.add_line_error(line_data, {'message': 'Found ", " in %s attribute, possible unescaped ",": "%s"' % (tag, value), 'error_type': 'FORMAT', 'location': ''}, log_level=logging.WARNING)
                                # In addition to Parent, the Alias, Note, Dbxref and Ontology_term attributes can have multiple values.
                                if tag in line_data['attributes']: # if this tag has been seen before
                                    if tag == 'Note': # don't check for duplicate notes
                                        line_data['attributes'][tag].extend(value.split(','))
                                    else: # only add non duplicate values
                                        line_data['attributes'][tag].extend([s for s in value.split(',') if s not in line_data['attributes'][tag]])
                                else:
                                    line_data['attributes'][tag] = value.split(',')
                                # check for duplicate values
                                if tag != 'Note' and len(line_data['attributes'][tag]) != len(set(line_data['attributes'][tag])):
                                    count_values = [(len(list(group)), key) for key, group in groupby(sorted(line_data['attributes'][tag]))]
                                    self.add_line_error(line_data, {'message': '%s attribute has identical values (count, value): %s' % (tag, ', '.join(['(%d, %s)' % (c, v) for c, v in count_values if c > 1])), 'error_type': 'FORMAT', 'location': ''})
                                    # remove duplicate
                                    line_data['attributes'][tag] = list(set(line_data['attributes'][tag]))

                                if tag == 'Parent':
                                    for feature_id in line_data['attributes']['Parent']:
                                        try:
                                            line_data['parents'].append(features[feature_id])
                                            for ld in features[feature_id]:
                                                # no need to check if line_data in ld['children'], because it is impossible, each ld maps to only one feature_id, so the ld we get are all different
                                                ld['children'].append(line_data)
                                        except KeyError: # features[id]
                                            self.add_line_error(line_data, {'message': '%s attribute has unresolved forward reference: %s' % (tag, feature_id), 'error_type': 'FORMAT', 'location': ''})
                                            unresolved_parents[feature_id].append(line_data)
                            elif tag == 'Target':
                                if value.find(',') >= 0:
                                    self.add_line_error(line_data, {'message': 'Value of %s attribute contains unescaped ",": "%s"' % (tag, value), 'error_type': 'FORMAT', 'location': ''})
                                target_tokens = value.split(' ')
                                if len(target_tokens) < 3 or len(target_tokens) > 4:
                                    self.add_line_error(line_data, {'message': 'Target attribute should have 3 or 4 values, got %d: %s' % (len(target_tokens), repr(tokens)), 'error_type': 'FORMAT', 'location': ''})
                                line_data['attributes'][tag] = {}
                                try:
                                    line_data['attributes'][tag]['target_id'] = target_tokens[0]
                                    all_good = True
                                    try:
                                        line_data['attributes'][tag]['start'] = int(target_tokens[1])
                                        if line_data['attributes'][tag]['start'] < 1:
                                            self.add_line_error(line_data, {'message': 'Start value of Target attribute is not a valid 1-based integer coordinate: "%s"' % target_tokens[1], 'error_type': 'FORMAT', 'location': ''})
                                    except ValueError:
                                        all_good = False
                                        line_data['attributes'][tag]['start'] = target_tokens[1]
                                        self.add_line_error(line_data, {'message': 'Start value of Target attribute is not a valid integer: "%s"' % line_data['attributes'][tag]['start'], 'error_type': 'FORMAT', 'location': ''})
                                    try:
                                        line_data['attributes'][tag]['end'] = int(target_tokens[2])
                                        if line_data['attributes'][tag]['end'] < 1:
                                            self.add_line_error(line_data, {'message': 'End value of Target attribute is not a valid 1-based integer coordinate: "%s"' % target_tokens[2], 'error_type': 'FORMAT', 'location': ''})
                                    except ValueError:
                                        all_good = False
                                        line_data['attributes'][tag]['end'] = target_tokens[2]
                                        self.add_line_error(line_data, {'message': 'End value of Target attribute is not a valid integer: "%s"' % line_data['attributes'][tag]['end'], 'error_type': 'FORMAT', 'location': ''})
                                    # if all_good then both start and end are int, so we can check if start is not less than or equal to end
                                    if all_good and line_data['attributes'][tag]['start'] > line_data['attributes'][tag]['end']:
                                        self.add_line_error(line_data, {'message': 'Start is not less than or equal to end', 'error_type': 'FORMAT', 'location': ''})
                                    line_data['attributes'][tag]['strand'] = target_tokens[3]
                                    if line_data['attributes'][tag]['strand'] not in valid_attribute_target_strand: # set(['+', '-', ''])
                                        self.add_line_error(line_data, {'message': 'Strand value of Target attribute has illegal characters: "%s"' % line_data['attributes'][tag]['strand'], 'error_type': 'FORMAT', 'location': ''})
                                except IndexError:
                                    pass
                            else:
                                if value.find(',') >= 0:
                                    self.add_line_error(line_data, {'message': 'Value of %s attribute contains unescaped ",": "%s"' % (tag, value), 'error_type': 'FORMAT', 'location': ''})
                                line_data['attributes'][tag] = value
                                if tag == 'Is_circular' and value != 'true':
                                    self.add_line_error(line_data, {'message': 'Value of Is_circular attribute is not "true": "%s"' % value, 'error_type': 'FORMAT', 'location': ''})
                                elif tag[:1].isupper() and tag not in reserved_attributes: # {'ID', 'Name', 'Alias', 'Parent', 'Target', 'Gap', 'Derives_from', 'Note', 'Dbxref', 'Ontology_term', 'Is_circular'}
                                    self.add_line_error(line_data, {'message': 'Unknown reserved (uppercase) attribute: "%s"' % tag, 'error_type': 'FORMAT', 'location': ''})
                                elif tag == 'ID':
                                    # check for duplicate ID in non-adjacent lines
                                    if value in features and lines[-1]['attributes'][tag] != value:
                                        self.add_line_error(line_data, {'message': 'Duplicate ID: "%s" in non-adjacent lines: %s' % (value, ','.join([str(f['line_index'] + 1) for f in features[value]])), 'error_type': 'FORMAT', 'location': ''}, log_level=logging.WARNING)
                                    features[value].append(line_data)
                except IndexError:
                    pass
            current_line_num += 1
            lines.append(line_data)

        if isinstance(gff_file, str):
            gff_fp.close()

        # global look up of unresolved parents
        for feature_id in unresolved_parents:
            if feature_id in features:
                for line in unresolved_parents[feature_id]:
                    self.add_line_error(line, {'message': 'Unresolved forward reference: "%s", found defined in lines: %s' % (feature_id, ','.join([str(ld['line_index'] + 1) for ld in features[feature_id]])), 'error_type': 'FORMAT', 'location': ''})

        self.lines = lines
        self.features = features
        return 1