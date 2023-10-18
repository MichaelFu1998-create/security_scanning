def get_command(self, ctx, name):
        """Retrieve the appropriate method from the Resource,
        decorate it as a click command, and return that method.
        """
        # Sanity check: Does a method exist corresponding to this
        # command? If not, None is returned for click to raise
        # exception.
        if not hasattr(self.resource, name):
            return None

        # Get the method.
        method = getattr(self.resource, name)

        # Get any attributes that were given at command-declaration
        # time.
        attrs = getattr(method, '_cli_command_attrs', {})

        # If the help message comes from the docstring, then
        # convert it into a message specifically for this resource.
        help_text = inspect.getdoc(method)
        attrs['help'] = self._auto_help_text(help_text or '')

        # On some methods, we ignore the defaults, which are intended
        # for writing and not reading; process this.
        ignore_defaults = attrs.pop('ignore_defaults', False)

        # Wrap the method, such that it outputs its final return
        # value rather than returning it.
        new_method = self._echo_method(method)

        # Soft copy the "__click_params__", if any exist.
        # This is the internal holding method that the click library
        # uses to store @click.option and @click.argument directives
        # before the method is converted into a command.
        #
        # Because self._echo_method uses @functools.wraps, this is
        # actually preserved; the purpose of copying it over is
        # so we can get our resource fields at the top of the help;
        # the easiest way to do this is to load them in before the
        # conversion takes place. (This is a happy result of Armin's
        # work to get around Python's processing decorators
        # bottom-to-top.)
        click_params = getattr(method, '__click_params__', [])
        new_method.__click_params__ = copy(click_params)
        new_method = with_global_options(new_method)

        # Write options based on the fields available on this resource.
        fao = attrs.pop('use_fields_as_options', True)
        if fao:
            for field in reversed(self.resource.fields):
                if not field.is_option:
                    continue

                # If we got an iterable rather than a boolean,
                # then it is a list of fields to use; check for
                # presence in that list.
                if not isinstance(fao, bool) and field.name not in fao:
                    continue

                # Create the initial arguments based on the
                # option value. If we have a different key to use
                # (which is what gets routed to the Tower API),
                # ensure that is the first argument.
                args = [field.option]
                if field.key:
                    args.insert(0, field.key)

                # short name aliases for common flags
                short_fields = {
                    'name': 'n',
                    'description': 'd',
                    'inventory': 'i',
                    'extra_vars': 'e'
                }
                if field.name in short_fields:
                    args.append('-'+short_fields[field.name])

                # Apply the option to the method.
                option_help = field.help
                if isinstance(field.type, StructuredInput):
                    option_help += ' Use @ to get JSON or YAML from a file.'
                if field.required:
                    option_help = '[REQUIRED] ' + option_help
                elif field.read_only:
                    option_help = '[READ ONLY] ' + option_help
                option_help = '[FIELD]' + option_help
                click.option(
                    *args,
                    default=field.default if not ignore_defaults else None,
                    help=option_help,
                    type=field.type,
                    show_default=field.show_default,
                    multiple=field.multiple,
                    is_eager=False
                )(new_method)

        # Make a click Command instance using this method
        # as the callback, and return it.
        cmd = click.command(name=name, cls=ActionSubcommand, **attrs)(new_method)

        # If this method has a `pk` positional argument,
        # then add a click argument for it.
        code = six.get_function_code(method)
        if 'pk' in code.co_varnames:
            click.argument('pk', nargs=1, required=False, type=str, metavar='[ID]')(cmd)

        # Done; return the command.
        return cmd