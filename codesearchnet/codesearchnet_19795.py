def check_parent_boundary(self):
        """
        checks whether child features are within the coordinate boundaries of parent features

        :return:
        """
        for line in self.lines:
            for parent_feature in line['parents']:
                ok = False
                for parent_line in parent_feature:
                    if parent_line['start'] <= line['start'] and line['end'] <= parent_line['end']:
                        ok = True
                        break
                if not ok:
                    self.add_line_error(line, {'message': 'This feature is not contained within the feature boundaries of parent: {0:s}: {1:s}'.format(
                        parent_feature[0]['attributes']['ID'],
                        ','.join(['({0:s}, {1:d}, {2:d})'.format(line['seqid'], line['start'], line['end']) for line in parent_feature])
                    ), 'error_type': 'BOUNDS', 'location': 'parent_boundary'})