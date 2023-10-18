def root(self, scope, names):
        """Find root of identifier, from scope
        args:
            scope (Scope): current scope
            names (list): identifier name list (, separated identifiers)
        returns:
            list
        """
        parent = scope.scopename
        if parent:
            parent = parent[-1]
            if parent.parsed:
                parsed_names = []
                for name in names:
                    ampersand_count = name.count('&')
                    if ampersand_count:
                        filtered_parts = []
                        for part in parent.parsed:
                            if part and part[0] not in self._subp:
                                filtered_parts.append(part)
                        permutations = list(
                            utility.permutations_with_replacement(
                                filtered_parts, ampersand_count))
                        for permutation in permutations:
                            parsed = []
                            for name_part in name:
                                if name_part == "&":
                                    parent_part = permutation.pop(0)
                                    if parsed and parsed[-1].endswith(']'):
                                        parsed.extend(' ')
                                    if parent_part[-1] == ' ':
                                        parent_part.pop()
                                    parsed.extend(parent_part)
                                else:
                                    parsed.append(name_part)
                            parsed_names.append(parsed)
                    else:
                        # NOTE(saschpe): Maybe this code can be expressed with permutations too?
                        for part in parent.parsed:
                            if part and part[0] not in self._subp:
                                parsed = []
                                if name[0] == "@media":
                                    parsed.extend(name)
                                else:
                                    parsed.extend(part)
                                    if part[-1] != ' ':
                                        parsed.append(' ')
                                    parsed.extend(name)
                                parsed_names.append(parsed)
                            else:
                                parsed_names.append(name)
                return parsed_names
        return names