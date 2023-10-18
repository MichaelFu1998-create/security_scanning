def handle(self, *args, **options):
        """Run the management command."""
        self.stdout.write('Clear index:')
        for model in get_registered_model():
            if options.get('model', None) and not (model.__name__ in
                                                   options['model']):
                continue

            clear_index(model)
            self.stdout.write('\t* {}'.format(model.__name__))