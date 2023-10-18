def p_statement_import(self, p):
        """ import_statement     : css_import t_ws string t_semicolon
                                 | css_import t_ws css_string t_semicolon
                                 | css_import t_ws css_string media_query_list t_semicolon
                                 | css_import t_ws fcall t_semicolon
                                 | css_import t_ws fcall media_query_list t_semicolon
        """
        #import pdb; pdb.set_trace()
        if self.importlvl > 8:
            raise ImportError(
                'Recrusive import level too deep > 8 (circular import ?)')
        if isinstance(p[3], string_types):
            ipath = utility.destring(p[3])
        elif isinstance(p[3], list):
            p[3] = Import(p[3], p.lineno(4)).parse(self.scope)
            ipath = utility.destring(p[3])
        elif isinstance(p[3], Call):
            # NOTE(saschpe): Always in the form of 'url("...");', so parse it
            # and retrieve the inner css_string. This whole func is messy.
            p[3] = p[3].parse(
                self.scope)  # Store it as string, Statement.fmt expects it.
            ipath = utility.destring(p[3][4:-1])
        fn, fe = os.path.splitext(ipath)
        if not fe or fe.lower() == '.less':
            try:
                cpath = os.path.dirname(os.path.abspath(self.target))
                if not fe:
                    ipath += '.less'
                filename = "%s%s%s" % (cpath, os.sep, ipath)
                if os.path.exists(filename):
                    recurse = LessParser(
                        importlvl=self.importlvl + 1,
                        verbose=self.verbose,
                        scope=self.scope)
                    recurse.parse(filename=filename, debuglevel=0)
                    p[0] = recurse.result
                else:
                    err = "Cannot import '%s', file not found" % filename
                    self.handle_error(err, p.lineno(1), 'W')
                    p[0] = None
            except ImportError as e:
                self.handle_error(e, p)
        else:
            p[0] = Statement(list(p)[1:], p.lineno(1))
            p[0].parse(None)
        sys.stdout.flush()