def set_mongonaut_base(self):
        """ Sets a number of commonly used attributes """
        if hasattr(self, "app_label"):
            # prevents us from calling this multiple times
            return None
        self.app_label = self.kwargs.get('app_label')
        self.document_name = self.kwargs.get('document_name')

        # TODO Allow this to be assigned via url variable
        self.models_name = self.kwargs.get('models_name', 'models')

        # import the models file
        self.model_name = "{0}.{1}".format(self.app_label, self.models_name)
        self.models = import_module(self.model_name)