def load_command_table(self, args): #pylint: disable=too-many-statements
        """Load all Service Fabric commands"""

        # Need an empty client for the select and upload operations
        with CommandSuperGroup(__name__, self,
                               'rcctl.custom_cluster#{}') as super_group:
            with super_group.group('cluster') as group:
                group.command('select', 'select')

        with CommandSuperGroup(__name__, self, 'rcctl.custom_reliablecollections#{}',
                               client_factory=client_create) as super_group: 
            with super_group.group('dictionary') as group:
                group.command('query', 'query_reliabledictionary')
                group.command('execute', 'execute_reliabledictionary')
                group.command('schema', 'get_reliabledictionary_schema')
                group.command('list', 'get_reliabledictionary_list')
                group.command('type-schema', 'get_reliabledictionary_type_schema')

        with ArgumentsContext(self, 'dictionary') as ac:
            ac.argument('application_name', options_list=['--application-name', '-a'])
            ac.argument('service_name', options_list=['--service-name', '-s'])
            ac.argument('dictionary_name', options_list=['--dictionary-name', '-d'])
            ac.argument('output_file', options_list=['--output-file', '-out'])
            ac.argument('input_file', options_list=['--input-file', '-in'])
            ac.argument('query_string', options_list=['--query-string', '-q'])
            ac.argument('type_name', options_list=['--type-name', '-t'])
        
        return OrderedDict(self.command_table)