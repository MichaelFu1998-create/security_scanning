def handle(self, *args, **options):
        """Run the management command."""
        batch_size = options.get('batchsize', None)
        if not batch_size:
            # py34-django18: batchsize is set to None if the user don't set
            # the value, instead of not be present in the dict
            batch_size = 1000

        self.stdout.write('The following models were reindexed:')
        for model in get_registered_model():
            if options.get('model', None) and not (model.__name__ in
                                                   options['model']):
                continue

            counts = reindex_all(model, batch_size=batch_size)
            self.stdout.write('\t* {} --> {}'.format(model.__name__, counts))