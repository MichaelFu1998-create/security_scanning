def set_mongoadmin(self):
        """ Returns the MongoAdmin object for an app_label/document_name style view
        """
        if hasattr(self, "mongoadmin"):
            return None

        if not hasattr(self, "document_name"):
            self.set_mongonaut_base()

        for mongoadmin in self.get_mongoadmins():
            for model in mongoadmin['obj'].models:
                if model.name == self.document_name:
                    self.mongoadmin = model.mongoadmin
                    break
        # TODO change this to use 'finally' or 'else' or something
        if not hasattr(self, "mongoadmin"):
            raise NoMongoAdminSpecified("No MongoAdmin for {0}.{1}".format(self.app_label, self.document_name))