def export(self, model_name, export_folder):
        """
        Export model and transformers to export_folder

        Parameters
        ----------
        model_name: string
            name of model to export
        export_folder: string
            folder to store exported model and transformers
        """
        for transformer in self.transformers:
            if isinstance(transformer, MultiLabelBinarizer):
                joblib.dump(transformer,
                            join(export_folder, "label.transformer.bin"),
                            protocol=2)
            if isinstance(transformer, TfidfVectorizer):
                joblib.dump(transformer,
                            join(export_folder, "tfidf.transformer.bin"),
                            protocol=2)
            if isinstance(transformer, CountVectorizer):
                joblib.dump(transformer,
                            join(export_folder, "count.transformer.bin"),
                            protocol=2)
            if isinstance(transformer, NumberRemover):
                joblib.dump(transformer,
                            join(export_folder, "number.transformer.bin"),
                            protocol=2)
        model = [model for model in self.models if model.name == model_name][0]
        e = Experiment(self.X, self.y, model.estimator, None)
        model_filename = join(export_folder, "model.bin")
        e.export(model_filename)