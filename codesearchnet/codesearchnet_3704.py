def format_options(self, ctx, formatter):
        """Monkey-patch click's format_options method to support option categorization.
        """
        field_opts = []
        global_opts = []
        local_opts = []
        other_opts = []
        for param in self.params:
            if param.name in SETTINGS_PARMS:
                opts = global_opts
            elif getattr(param, 'help', None) and param.help.startswith('[FIELD]'):
                opts = field_opts
                param.help = param.help[len('[FIELD]'):]
            else:
                opts = local_opts
            rv = param.get_help_record(ctx)
            if rv is None:
                continue
            else:
                opts.append(rv)

        if self.add_help_option:
            help_options = self.get_help_option_names(ctx)
            if help_options:
                other_opts.append([join_options(help_options)[0], 'Show this message and exit.'])

        if field_opts:
            with formatter.section('Field Options'):
                formatter.write_dl(field_opts)
        if local_opts:
            with formatter.section('Local Options'):
                formatter.write_dl(local_opts)
        if global_opts:
            with formatter.section('Global Options'):
                formatter.write_dl(global_opts)
        if other_opts:
            with formatter.section('Other Options'):
                formatter.write_dl(other_opts)