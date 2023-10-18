def adopt(self, old_parent, new_parent):
        """
        Transfer children from old_parent to new_parent

        :param old_parent: feature_id(str) or line_index(int) or line_data(dict) or feature
        :param new_parent: feature_id(str) or line_index(int) or line_data(dict)
        :return: List of children transferred
        """
        try: # assume line_data(dict)
            old_id = old_parent['attributes']['ID']
        except TypeError:
            try: # assume line_index(int)
                old_id = self.lines[old_parent]['attributes']['ID']
            except TypeError: # assume feature_id(str)
                old_id = old_parent
        old_feature = self.features[old_id]
        old_indexes = [ld['line_index'] for ld in old_feature]
        try: # assume line_data(dict)
            new_id = new_parent['attributes']['ID']
        except TypeError:
            try: # assume line_index(int)
                new_id = self.lines[new_parent]['attributes']['ID']
            except TypeError: # assume feature_id(str)
                new_id = new_parent
        new_feature = self.features[new_id]
        new_indexes = [ld['line_index'] for ld in new_feature]
        # build a list of children to be moved
        # add the child to the new parent's children list if its not already there
        # update the child's parent list and parent attribute
        # finally remove the old parent's children list
        children = old_feature[0]['children']
        new_parent_children_set = set([ld['line_index'] for ld in new_feature[0]['children']])
        for child in children:
            if child['line_index'] not in new_parent_children_set:
                new_parent_children_set.add(child['line_index'])
                for new_ld in new_feature:
                    new_ld['children'].append(child)
                child['parents'].append(new_feature)
                child['attributes']['Parent'].append(new_id)
            # remove multiple, list.remove() only removes 1
            child['parents'] = [f for f in child['parents'] if f[0]['attributes']['ID'] != old_id]
            child['attributes']['Parent'] = [d for d in child['attributes']['Parent'] if d != old_id]
        for old_ld in old_feature:
            old_ld['children'] = []
        return children