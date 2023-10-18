def _pprint(self, cycle=False, flat=False, annotate=False, onlychanged=True, level=1, tab = '   '):
        """
        Pretty printer that prints only the modified keywords and
        generates flat representations (for repr) and optionally
        annotates the top of the repr with a comment.
        """
        (kwargs, pos_args, infix_operator, extra_params) = self._pprint_args
        (br, indent)  = ('' if flat else '\n', '' if flat else tab * level)
        prettify = lambda x: isinstance(x, PrettyPrinted) and not flat
        pretty = lambda x: x._pprint(flat=flat, level=level+1) if prettify(x) else repr(x)

        params = dict(self.get_param_values())
        show_lexsort = getattr(self, '_lexorder', None) is not None
        modified = [k for (k,v) in self.get_param_values(onlychanged=onlychanged)]
        pkwargs = [(k, params[k])  for k in kwargs if (k in modified)] + list(extra_params.items())
        arg_list = [(k,params[k]) for k in pos_args] + pkwargs

        lines = []
        if annotate: # Optional annotating comment
            len_ckeys, len_vkeys = len(self.constant_keys), len(self.varying_keys)
            info_triple = (len(self),
                           ', %d constant key(s)' % len_ckeys if len_ckeys else '',
                           ', %d varying key(s)'  % len_vkeys if len_vkeys else '')
            annotation = '# == %d items%s%s ==\n' % info_triple
            lines = [annotation]

        if show_lexsort: lines.append('(')
        if cycle:
            lines.append('%s(...)' % self.__class__.__name__)
        elif infix_operator:
            level = level - 1
            triple = (pretty(params[pos_args[0]]), infix_operator, pretty(params[pos_args[1]]))
            lines.append('%s %s %s' % triple)
        else:
            lines.append('%s(' % self.__class__.__name__)
            for (k,v) in arg_list:
                lines.append('%s%s=%s' %  (br+indent, k, pretty(v)))
                lines.append(',')
            lines = lines[:-1] +[br+(tab*(level-1))+')'] # Remove trailing comma

        if show_lexsort:
            lines.append(').lexsort(%s)' % ', '.join(repr(el) for el in self._lexorder))
        return ''.join(lines)